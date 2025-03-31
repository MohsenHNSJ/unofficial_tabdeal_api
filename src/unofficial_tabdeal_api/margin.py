"""This module holds the MarginClass."""

from typing import Any

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import (
    GET_ALL_MARGIN_OPEN_ORDERS_URI,
    GET_MARGIN_ASSET_DETAILS_PRT1,
    GET_MARGIN_ASSET_DETAILS_PRT2,
)


class MarginClass(BaseClass):
    """This is the class storing methods related to Margin trading."""

    async def get_margin_asset_id(self, isolated_symbol: str) -> int:
        """Gets the ID of a margin asset from server and returns it as an integer.

        Returns -1 in case of an error

        Args:
            isolated_symbol (str): Isolated symbol of margin asset.
            example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            int: Margin asset ID as integer
        """
        self._logger.debug(
            "Trying to get margin asset ID for [%s]",
            isolated_symbol,
        )

        connection_url: str = (
            GET_MARGIN_ASSET_DETAILS_PRT1 + isolated_symbol + GET_MARGIN_ASSET_DETAILS_PRT2
        )

        margin_asset_id: int

        # We get the data from server and save it in a temporary variable
        temp_variable = await self._get_data_from_server(connection_url)

        # If the data from server is not what we expect, we print an error
        # and return [-1]
        if temp_variable is None:
            self._logger.error(
                "Failed to get margin asset ID for [%s]. Server response is [None]! Returning [-1]",
                isolated_symbol,
            )

            return -1

        # Else, the server response must be OK
        # so we assign the asset ID and return it
        margin_asset_id = temp_variable["id"]  # type: ignore[call-overload]
        self._logger.debug("Margin asset ID: [%s]", margin_asset_id)

        return margin_asset_id

    async def get_all_open_margin_orders(self) -> list[dict[str, Any]] | None:
        """Gets all the open margin orders from server and returns it as a list of dictionaries.

        Returns `None` in case of an error

        Returns:
            list[dict[str, Any]] | None: a List of dictionary items or `None` in case of an error
        """
        self._logger.debug("Trying to get all open margin orders")

        # We get the data from server and save it in a temporary variable
        all_open_margin_orders = await self._get_data_from_server(GET_ALL_MARGIN_OPEN_ORDERS_URI)

        # If the data from server is not what we expect, we print an error
        if all_open_margin_orders is None:
            self._logger.error(
                "Failed to get all open margin orders! Returning server response: [%s]",
                all_open_margin_orders,
            )
        # Else, the server response must be OK
        else:
            self._logger.debug(
                "List of all open margin orders has [%s] items",
                len(all_open_margin_orders),
            )

        return all_open_margin_orders  # type: ignore[return-value]
