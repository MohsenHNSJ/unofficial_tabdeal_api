"""This module holds the WalletClass."""

from decimal import Decimal

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import (
    GET_WALLET_USDT_BALANCE_QUERY,
    GET_WALLET_USDT_BALANCE_URI,
)
from unofficial_tabdeal_api.utils import normalize_decimal


class WalletClass(BaseClass):
    """This is the class storing methods related to account wallet."""

    async def get_wallet_usdt_balance(self) -> Decimal:
        """Gets the balance of wallet in USDT and returns it as Decimal.

        Returns:
            Decimal: Wallet USDT balance in Decimal
        """
        self._logger.debug("Trying to get wallet balance")

        # We get the data from server
        wallet_details = await self._get_data_from_server(
            connection_url=GET_WALLET_USDT_BALANCE_URI,
            queries=GET_WALLET_USDT_BALANCE_QUERY,
        )

        # If the type is correct, we log and return the data
        if isinstance(wallet_details, dict):
            wallet_usdt_balance: Decimal = await normalize_decimal(
                Decimal(str(wallet_details["TetherUS"])),
            )

            self._logger.debug(
                "Wallet balance retrieved successfully, [%s] $",
                wallet_usdt_balance,
            )

            return wallet_usdt_balance

        # Else, we log and raise TypeError
        self._logger.error(
            "Expected dictionary, got [%s]",
            type(wallet_details),
        )

        raise TypeError
