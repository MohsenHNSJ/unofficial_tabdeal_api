"""This module holds the MarginClass."""

from decimal import Decimal
from typing import Any

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import (
    GET_ALL_MARGIN_OPEN_ORDERS_URI,
    GET_MARGIN_ASSET_DETAILS_PRT1,
    GET_MARGIN_ASSET_DETAILS_PRT2,
)
from unofficial_tabdeal_api.utils import normalize_decimal


class MarginClass(BaseClass):
    """This is the class storing methods related to Margin trading."""

    async def _get_isolated_symbol_details(self, isolated_symbol: str) -> dict[str, Any] | None:
        """Gets the full details of an isolated symbol from server and returns it as a dictionary.

        Returns None in case of an error

        Args:
            isolated_symbol (str): Isolated symbol of margin asset.
            example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            dict[str, Any] | None: Isolated symbol details or none in case of an error
        """
        self._logger.debug("Trying to get details of [%s]", isolated_symbol)

        # We create the connection url
        connection_url: str = (
            GET_MARGIN_ASSET_DETAILS_PRT1 + isolated_symbol + GET_MARGIN_ASSET_DETAILS_PRT2
        )

        # We get the data from server and save it in a temporary variable
        temp_variable = await self._get_data_from_server(connection_url)

        # If the data from server is what we expect, we return the data
        if isinstance(temp_variable, dict):
            self._logger.debug(
                "Isolated symbol [%s] details retrieved successfully",
                isolated_symbol,
            )
            return temp_variable
        # Else, the data from server is not what we expect, we print an error and return None
        self._logger.error(
            "Failed to get Isolated symbol details [%s]",
            isolated_symbol,
        )
        return None

    async def get_all_open_orders(self) -> list[dict[str, Any]] | None:
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

    async def get_asset_id(self, isolated_symbol: str) -> int:
        """Gets the ID of a margin asset from server and returns it as an integer.

        Returns -1 in case of an error

        Args:
            isolated_symbol (str): Isolated symbol of margin asset.
            example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            int: Margin asset ID as integer
        """
        temp_variable: dict[str, Any] | None = await self._get_isolated_symbol_details(
            isolated_symbol,
        )

        margin_asset_id: int = -1

        # if the data from server is what we expect, we proceed and process it
        if isinstance(temp_variable, dict):
            # We extract the asset ID
            margin_asset_id = temp_variable["id"]
            self._logger.debug("Margin asset ID: [%s]", margin_asset_id)
        # Else, the server response must be INVALID
        else:
            self._logger.error(
                "Failed to get margin asset ID for [%s]. Server response is [None]! Returning [-1]",
                isolated_symbol,
            )

        return margin_asset_id

    async def get_break_even_price(self, asset_id: int) -> Decimal | None:
        """Gets the price point for an order which Tabdeal says it yields no profit and loss.

        Returns None in case of an error

        Args:
            asset_id (int): Margin asset ID got from get_asset_id() function

        Returns:
            Decimal | None: Either returns the price as Decimal or returns None in case of an error
        """
        self._logger.debug(
            "Trying to get break even price for margin asset with ID:[%s]",
            asset_id,
        )

        # First we get all margin open orders
        all_margin_open_orders: list[dict[str, Any]] | None = await self.get_all_open_orders()

        # If the data from server is not what we expect, we print an error and return [None]
        if all_margin_open_orders is None:
            self._logger.error("Failed to get all open margin order!")

            return None

        # Then we search through the list and find the asset ID we are looking for
        # And store that into our variable
        # Get the first object in a list that meets a condition, if nothing found, return [None]
        margin_order: dict[str, Any] | None = next(
            (
                order_status
                for order_status in all_margin_open_orders
                if order_status["id"] == asset_id
            ),
            None,
        )

        # If no match found in the server response, return [None]
        if margin_order is None:
            self._logger.error(
                "Break even price not found for asset ID [%s]! Returning [None]",
                asset_id,
            )

            return None

        # Else, we should have found a result, so we extract the break even price,
        # normalize and return it
        break_even_price: Decimal = await normalize_decimal(
            Decimal(str(margin_order["break_even_point"])),
        )

        self._logger.debug("Break even price found as [%s]", break_even_price)

        return break_even_price

    async def get_pair_id(self, isolated_symbol: str) -> int:
        """Gets the pair ID for a margin asset from server and returns it as an integer.

        Returns -1 in case of an error

        Args:
            isolated_symbol (str): Isolated symbol of margin asset.
            example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            int: Margin pair ID an integer
        """
        temp_variable: dict[str, Any] | None = await self._get_isolated_symbol_details(
            isolated_symbol,
        )

        margin_pair_id: int = -1

        # If the data from server is what we expect, we proceed and process it
        if isinstance(temp_variable, dict):
            # First we extract pair information
            margin_pair_information = temp_variable["pair"]
            # Then we extract the pair ID
            margin_pair_id = margin_pair_information["id"]
            self._logger.debug("Margin pair ID is [%s]", margin_pair_id)
        # Else, the server response must be INVALID
        else:
            self._logger.error(
                "Failed to get margin asset ID for [%s]. Server response is [None]! Returning [-1]",
                isolated_symbol,
            )

        return margin_pair_id
