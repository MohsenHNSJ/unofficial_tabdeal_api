"""This module holds the WalletClass."""
# pylint: disable=R0903

from decimal import Decimal
from typing import Any

from pydantic import ValidationError

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import (
    GET_WALLET_USDT_BALANCE_QUERY,
    GET_WALLET_USDT_BALANCE_URI,
    TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_URI,
    TRANSFER_USDT_TO_MARGIN_ASSET_URI,
)
from unofficial_tabdeal_api.models import (
    TransferFromMarginModel,
    TransferToMarginModel,
    WalletDetailsModel,
)
from unofficial_tabdeal_api.utils import isolated_symbol_to_tabdeal_symbol, normalize_decimal


class WalletClass(BaseClass):
    """This is the class storing methods related to account wallet."""

    async def get_wallet_usdt_balance(self) -> Decimal:
        """Gets the balance of wallet in USDT and returns it as Decimal.

        Returns:
            Decimal: Wallet USDT balance in Decimal
        """
        self._logger.debug("Trying to get wallet balance")

        # We get the data from server
        wallet_details: dict[str, Any] | list[dict[str, Any]] = await self._get_data_from_server(
            connection_url=GET_WALLET_USDT_BALANCE_URI,
            queries=GET_WALLET_USDT_BALANCE_QUERY,
        )

        # If the response is not a dictionary, we log and raise TypeError
        if not isinstance(wallet_details, dict):
            self._logger.error(
                "Expected dictionary, got [%s]",
                type(wallet_details),
            )
            raise TypeError

        try:
            validated = WalletDetailsModel(**wallet_details)
            wallet_usdt_balance: Decimal = normalize_decimal(
                validated.tether_us,
            )

            self._logger.debug(
                "Wallet balance retrieved successfully, [%s] $",
                wallet_usdt_balance,
            )

        except (ValidationError, TypeError) as e:
            # If the data is not valid, we log and raise TypeError
            self._logger.exception(
                "Failed to validate wallet details",
            )
            raise TypeError from e

        return wallet_usdt_balance

    async def transfer_usdt_from_wallet_to_margin_asset(
        self,
        *,
        transfer_amount: Decimal,
        isolated_symbol: str,
    ) -> None:
        """Transfers USDT from wallet to margin asset.

        Args:
            transfer_amount (Decimal): Amount of USDT to transfer
            isolated_symbol (str): Isolated symbol to transfer USDT to
        """
        self._logger.debug(
            "Trying to transfer [%s] USDT from wallet to margin asset [%s]",
            transfer_amount,
            isolated_symbol,
        )

        # We convert isolated symbol to tabdeal symbol
        tabdeal_symbol: str = isolated_symbol_to_tabdeal_symbol(
            isolated_symbol=isolated_symbol,
        )

        # We create the payload data
        try:
            payload = TransferToMarginModel(
                transfer_amount_from_main=transfer_amount,
                pair_symbol=tabdeal_symbol,
            )
            data = payload.model_dump_json()
        except ValidationError as e:
            # If the data is not valid, we log and raise TypeError
            self._logger.exception(
                "Failed to validate transfer data for USDT transfer to margin asset",
            )
            raise TypeError from e

        # Then, we send the request to the server
        _: dict[str, Any] | list[dict[str, Any]] = await self._post_data_to_server(
            connection_url=TRANSFER_USDT_TO_MARGIN_ASSET_URI,
            data=data,
        )

        # If we reach here, then the request was successful
        self._logger.debug(
            "Transfer of [%s] USDT from wallet to margin asset [%s] was successful",
            transfer_amount,
            isolated_symbol,
        )

    async def transfer_usdt_from_margin_asset_to_wallet(
        self,
        *,
        transfer_amount: Decimal,
        isolated_symbol: str,
    ) -> None:
        """Transfers USDT from margin asset to wallet.

        Args:
            transfer_amount (Decimal): Amount of USDT to transfer
            isolated_symbol (str): Isolated symbol to transfer USDT from
        """
        self._logger.debug(
            "Trying to transfer [%s] USDT from margin asset [%s] to wallet",
            transfer_amount,
            isolated_symbol,
        )

        # We create the payload data
        try:
            payload = TransferFromMarginModel(
                amount=transfer_amount,
                pair_symbol=isolated_symbol,
            )
            data = payload.model_dump_json()
        except ValidationError as e:
            # If the data is not valid, we log and raise TypeError
            self._logger.exception(
                "Failed to validate transfer data for USDT transfer from margin asset",
            )
            raise TypeError from e

        # Then we send the request to the server
        _: dict[str, Any] | list[dict[str, Any]] = await self._post_data_to_server(
            connection_url=TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_URI,
            data=data,
        )

        # If we reach here, then the request was successful
        self._logger.debug(
            "Transfer of [%s] USDT from margin asset [%s] to wallet was successful",
            transfer_amount,
            isolated_symbol,
        )
