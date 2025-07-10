"""This is the class of Tabdeal client."""

import asyncio
from typing import TYPE_CHECKING

from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.exceptions import MarginOrderNotFoundInActiveOrdersError
from unofficial_tabdeal_api.margin import MarginClass
from unofficial_tabdeal_api.models import MarginOrderModel
from unofficial_tabdeal_api.order import OrderClass
from unofficial_tabdeal_api.utils import calculate_sl_tp_prices
from unofficial_tabdeal_api.wallet import WalletClass

if TYPE_CHECKING:  # pragma: no cover
    from decimal import Decimal

    from unofficial_tabdeal_api.models import MarginOpenOrderModel


class TabdealClient(AuthorizationClass, MarginClass, WalletClass, OrderClass):
    """a client class to communicate with Tabdeal platform."""

    async def _validate_trade_conditions(self, order: MarginOrderModel) -> bool:
        """Validate trade conditions for a margin order.

        Args:
            order (MarginOrderModel): The margin order to validate.

        Returns:
            bool: True if the trade conditions are valid, False otherwise.
        """
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

        # Else, conditions are met, we can continue
        return True

    async def _open_order(self, order: MarginOrderModel) -> None:
        """Open a margin order.

        Args:
            order (MarginOrderModel): The margin order to open.

        Returns:
            None
        """
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

    async def _wait_for_order_fill(self, order: MarginOrderModel) -> bool:
        """Wait for the margin order to be filled.

        Args:
            order (MarginOrderModel): The margin order to wait for.

        Returns:
            bool: True if the order is filled, False otherwise.
        """
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
                "Margin order is not found in active margin orders list! Process will not continue",
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

        # If we reach this point, it means the order is filled
        return True

    async def _setup_stop_loss_take_profit(self, order: MarginOrderModel) -> int:
        """Setup stop loss and take profit for a margin order.

        Args:
            order (MarginOrderModel): The margin order to setup SL/TP for.

        Returns:
            int: The margin asset ID.
        """
        # Set SL/TP prices
        margin_asset_id: int = await self.get_margin_asset_id(isolated_symbol=order.isolated_symbol)
        # Get break-even point
        break_even_point: Decimal = await self.get_order_break_even_price(asset_id=margin_asset_id)
        # Get price precision requirements
        _, price_precision_required = await self.get_margin_asset_precision_requirements(
            isolated_symbol=order.isolated_symbol,
        )
        # Check if price precision is required
        price_fraction_allowed: bool = price_precision_required != 0
        # Calculate stop loss and take profit points
        stop_loss_point, take_profit_point = calculate_sl_tp_prices(
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
        # Set stop loss and take profit for the margin order
        await self.set_sl_tp_for_margin_order(
            margin_asset_id=margin_asset_id,
            stop_loss_price=stop_loss_point,
            take_profit_price=take_profit_point,
        )

        return margin_asset_id

    async def _wait_for_order_close(self, margin_asset_id: int) -> None:
        """Wait for the margin order to close.

        Args:
            margin_asset_id (int): The ID of the margin asset to wait for.
        """
        # Wait until it hit SL or TP price and order close
        # If margin order hit's SL or TP points, it closes and will not be
        # in active margin orders list
        is_order_closed: bool = False

        while is_order_closed is False:
            all_margin_open_orders: list[
                MarginOpenOrderModel
            ] = await self.get_margin_all_open_orders()

            # Then we search for the market ID of the asset we are trading
            # Get the first object in a list that meets a condition, if nothing found, return None
            search_result: MarginOpenOrderModel | None = None
            for open_order in all_margin_open_orders:
                if open_order.id == margin_asset_id:
                    search_result = open_order
                    break

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

    async def _withdraw_balance_if_requested(self, order: MarginOrderModel) -> None:
        """Withdraw balance from margin asset to wallet if requested.

        Args:
            order (MarginOrderModel): The margin order containing the asset symbol.
        """
        self._logger.debug("User asked to withdraw balance after trade")
        # Get asset balance
        asset_balance: Decimal = await self.get_margin_asset_balance(order.isolated_symbol)

        # Transfer all of asset balance to wallet
        await self.transfer_usdt_from_margin_asset_to_wallet(
            transfer_amount=asset_balance,
            isolated_symbol=order.isolated_symbol,
        )
        self._logger.debug("Transferring of asset balance to wallet done")

    async def trade_margin_order(  # pylint: disable=R0914
        self,
        *,
        order: MarginOrderModel,
        withdraw_balance_after_trade: bool,
    ) -> bool:
        """Trade a margin order.

        Args:
            order (MarginOrderModel): MarginOrderModel object containing order details.
            withdraw_balance_after_trade (bool): Flag indicating
                whether to withdraw balance after trade.

        Returns:
            bool: Whether the trade was successful or not.
        """
        self._logger.debug("Trade order received")

        # Validate trade conditions
        if not await self._validate_trade_conditions(order):
            return False

        # Prepare and open the order
        await self._open_order(order)

        # Order processing might take a bit of time by the server
        # So we wait for 3 seconds, before continuing the process
        await asyncio.sleep(delay=3)

        # Wait for order to be filled
        if not await self._wait_for_order_fill(order):
            return False

        # Setup stop loss and take profit
        margin_asset_id = await self._setup_stop_loss_take_profit(order)

        # Wait for order to close
        await self._wait_for_order_close(margin_asset_id)

        # Get the margin asset balance in USDT and withdraw all of it (Optional)
        if withdraw_balance_after_trade:
            # Withdraw balance if requested
            await self._withdraw_balance_if_requested(order)

        self._logger.debug("Trade finished")
        return True
