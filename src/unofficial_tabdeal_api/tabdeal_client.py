"""This is the class of Tabdeal client."""

import asyncio
from typing import TYPE_CHECKING, Any

from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.exceptions import MarginOrderNotFoundInActiveOrdersError
from unofficial_tabdeal_api.margin import MarginClass
from unofficial_tabdeal_api.order import MarginOrder, OrderClass
from unofficial_tabdeal_api.utils import calculate_sl_tp_prices
from unofficial_tabdeal_api.wallet import WalletClass

if TYPE_CHECKING:  # pragma: no cover
    from decimal import Decimal


class TabdealClient(AuthorizationClass, MarginClass, WalletClass, OrderClass):
    """a client class to communicate with Tabdeal platform."""

    async def _test(self) -> str:
        """Temporary test function."""
        return "test"

    async def trade_margin_order(
        self,
        *,
        order: MarginOrder,
        withdraw_balance_after_trade: bool,
    ) -> bool:
        """TODO: Unfinished function."""
        self._logger.debug("Trade order received")
        # Check if the margin asset already has an active order, if so, cancel this
        if await self.does_margin_asset_have_active_order(isolated_symbol=order.isolated_symbol):
            self._logger.warning(
                "An order is already open for [%s], This order will be skipped",
                order.isolated_symbol,
            )
            return False

        # Check if margin asset is trade-able, if not, cancel order
        if not await self.is_margin_asset_trade_able(isolated_symbol=order.isolated_symbol):
            self._logger.warning(
                "Margin asset [%s] is not trade-able on Tabdeal, This order will be skipped",
                order.isolated_symbol,
            )
            return False

        # Deposit funds into margin asset
        await self.transfer_usdt_from_wallet_to_margin_asset(
            transfer_amount=order.deposit_amount,
            isolated_symbol=order.isolated_symbol,
        )
        self._logger.debug(
            "[%s] funds deposited into [%s]",
            order.deposit_amount,
            order.isolated_symbol,
        )

        # Open margin order
        order_id: int = await self.open_margin_order(order=order)
        self._logger.debug("Order opened with ID: [%s]", order_id)

        # Order processing might take a bit of time by the server
        # So we wait for 3 seconds, before continuing the process
        await asyncio.sleep(delay=3)

        is_margin_order_filled: bool = False
        # Wait until it's fully filled (Check every 1 minute)
        # If MarginOrderNotFoundInActiveOrdersError is raised, stop the process
        # and try to withdraw the deposit
        try:
            while is_margin_order_filled is False:
                # Check if order is filled or not
                is_margin_order_filled = await self.is_margin_order_filled(
                    isolated_symbol=order.isolated_symbol,
                )
                self._logger.debug(
                    "Order fill status = [%s]",
                    is_margin_order_filled,
                )

                # If filled, go to the next loop, which means stop the loop
                if is_margin_order_filled:
                    continue

                # Else, Wait for 1 minute and try again
                self._logger.debug(
                    "Sleeping for one minute before trying again",
                )
                await asyncio.sleep(delay=60)

        except MarginOrderNotFoundInActiveOrdersError:
            self._logger.exception(
                "Margin order is not found in active margin orders list!Process will not continue",
            )

            self._logger.debug("Trying to withdraw deposited amount of USDT")
            # Try to withdraw the deposited money
            remaining_balance: Decimal = await self.get_margin_asset_balance(
                isolated_symbol=order.isolated_symbol,
            )

            await self.transfer_usdt_from_margin_asset_to_wallet(
                transfer_amount=remaining_balance,
                isolated_symbol=order.isolated_symbol,
            )
            self._logger.info(
                "Trading failed, but, "
                "Successfully withdrawn the remaining amount of USDT [%s] from asset [%s]",
                remaining_balance,
                order.isolated_symbol,
            )
            return False

        # Set SL/TP prices
        # Get break-even point
        margin_asset_id: int = await self.get_margin_asset_id(isolated_symbol=order.isolated_symbol)

        break_even_point: Decimal = await self.get_order_break_even_price(asset_id=margin_asset_id)

        _, price_precision_required = await self.get_margin_asset_precision_requirements(
            isolated_symbol=order.isolated_symbol,
        )

        price_fraction_allowed: bool = price_precision_required == 0

        stop_loss_point, take_profit_point = await calculate_sl_tp_prices(
            margin_level=order.margin_level,
            order_side=order.order_side,
            break_even_point=break_even_point,
            stop_loss_percent=order.stop_loss_percent,
            take_profit_percent=order.take_profit_percent,
            price_required_precision=price_precision_required,
            price_fraction_allowed=price_fraction_allowed,
        )
        self._logger.debug(
            "Stop loss point: [%s] - Take profit point: [%s]",
            stop_loss_point,
            take_profit_point,
        )

        await self.set_sl_tp_for_margin_order(
            margin_asset_id=margin_asset_id,
            stop_loss_price=stop_loss_point,
            take_profit_price=take_profit_point,
        )

        # Wait until it hit SL or TP price and order close
        # If margin order hit's SL or TP points, it closes and will not be
        # in active margin orders list
        is_order_closed: bool = False

        while is_order_closed is False:
            all_margin_open_orders: list[dict[str, Any]] = await self.get_margin_all_open_orders()

            # Then we search for the market ID of the asset we are trading
            # Get the first object in a list that meets a condition, if nothing found, return None
            search_result: dict[str, Any] | None = next(
                (
                    margin_order
                    for margin_order in all_margin_open_orders
                    if margin_order["id"] == margin_asset_id
                ),
                None,
            )

            # If the market ID is NOT found, it means the order is closed
            if search_result is None:
                self._logger.debug("Margin order seems to be closed")
                # We set the is order closed to True and continue to next loop to jump out
                is_order_closed = True

                continue

            # Else, the order is still running, we wait for 1 minute and repeat the loop
            self._logger.debug(
                "Margin order is not yet closed, waiting for one minute before trying again",
            )
            await asyncio.sleep(delay=60)

        # Get the margin asset balance in USDT and withdraw all of it (This should be optional)
        if withdraw_balance_after_trade:
            self._logger.debug("User asked to withdraw balance after trade")
            # Get asset balance
            asset_balance: Decimal = await self.get_margin_asset_balance(order.isolated_symbol)

            # Transfer all of asset balance to wallet
            await self.transfer_usdt_from_margin_asset_to_wallet(
                transfer_amount=asset_balance,
                isolated_symbol=order.isolated_symbol,
            )
            self._logger.debug("Transferring of asset balance to wallet done")

        self._logger.debug("Trade finished")
        return True
