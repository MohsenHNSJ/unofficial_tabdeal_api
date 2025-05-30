"""This is the class of Tabdeal client."""

import asyncio
from typing import TYPE_CHECKING

from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.exceptions import MarginOrderNotFoundInActiveOrdersError
from unofficial_tabdeal_api.margin import MarginClass
from unofficial_tabdeal_api.order import MarginOrder, OrderClass
from unofficial_tabdeal_api.wallet import WalletClass

if TYPE_CHECKING:
    from decimal import Decimal


class TabdealClient(AuthorizationClass, MarginClass, WalletClass, OrderClass):
    """a client class to communicate with Tabdeal platform."""

    async def _test(self) -> str:
        """Temporary test function."""
        return "test"

    async def trade_margin_order(self, *, order: MarginOrder) -> bool:
        """TODO: Unfinished function."""
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

                # If filled, go to the next loop, which means stop the loop
                if is_margin_order_filled:
                    continue

                # Else, Wait for 1 minute and try again
                await asyncio.sleep(delay=60)

        except MarginOrderNotFoundInActiveOrdersError:
            self._logger.exception(
                "Margin order is not found in active margin orders list!Process will not continue",
            )

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

        # Wait until it hit SL or TP price and order close

        # Get the margin asset balance in USDT and withdraw all of it (This should be optional)

        return True
