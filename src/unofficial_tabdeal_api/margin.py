"""This module holds the MarginClass."""

from decimal import Decimal
from typing import Any

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import (
    GET_ALL_MARGIN_OPEN_ORDERS_URI,
    GET_MARGIN_ASSET_DETAILS_PRT1,
    GET_MARGIN_ASSET_DETAILS_PRT2,
)
from unofficial_tabdeal_api.exceptions import (
    BreakEvenPriceNotFoundError,
    MarginTradingNotActiveError,
    MarketNotFoundError,
)
from unofficial_tabdeal_api.utils import normalize_decimal


class MarginClass(BaseClass):
    """This is the class storing methods related to Margin trading."""

    async def _get_isolated_symbol_details(self, isolated_symbol: str) -> dict[str, Any]:
        """Gets the full details of an isolated symbol from server and returns it as a dictionary.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset.
            example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            dict[str, Any]: Isolated symbol details
        """
        self._logger.debug("Trying to get details of [%s]", isolated_symbol)

        # We create the connection url
        connection_url: str = (
            GET_MARGIN_ASSET_DETAILS_PRT1 + isolated_symbol + GET_MARGIN_ASSET_DETAILS_PRT2
        )

        # We get the data from server
        isolated_symbol_details = await self._get_data_from_server(connection_url)

        # If the type is correct, we log and return the data
        if isinstance(isolated_symbol_details, dict):
            symbol_name: str = ((isolated_symbol_details["first_currency_credit"])["currency"])[
                "name"
            ]

            self._logger.debug(
                "Details retrieved successfully.\nSymbol name: [%s]",
                symbol_name,
            )

            return isolated_symbol_details

        # Else, we log and raise TypeError
        self._logger.error(
            "Expected dictionary, got [%s]",
            type(isolated_symbol_details),
        )
        raise TypeError

    async def get_all_open_orders(self) -> list[dict[str, Any]]:
        """Gets all the open margin orders from server and returns it as a list of dictionaries.

        Returns:
            list[dict[str, Any]]: a List of dictionary items
        """
        self._logger.debug("Trying to get all open margin orders")

        # We get the data from server
        all_open_orders = await self._get_data_from_server(GET_ALL_MARGIN_OPEN_ORDERS_URI)

        # If the type is correct, we log and return the data
        if isinstance(all_open_orders, list):
            self._logger.debug(
                "Data retrieved successfully.\nYou have [%s] open positions",
                len(all_open_orders),
            )

            return all_open_orders

        # Else, we log and raise TypeError
        self._logger.error("Expected list, got [%s]", type(all_open_orders))

        raise TypeError

    async def get_margin_asset_id(self, isolated_symbol: str) -> int:
        """Gets the ID of a margin asset from server and returns it as an integer.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset.
            example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            int: Margin asset ID as integer
        """
        self._logger.debug("Trying to get asset ID of [%s]", isolated_symbol)

        # We get the data from server
        isolated_symbol_details: dict[str, Any] = await self._get_isolated_symbol_details(
            isolated_symbol,
        )

        # We Extract the asset ID and return it
        margin_asset_id: int = isolated_symbol_details["id"]
        self._logger.debug("Margin asset ID: [%s]", margin_asset_id)

        return margin_asset_id

    async def get_order_break_even_price(self, asset_id: int) -> Decimal:
        """Gets the price point for an order which Tabdeal says it yields no profit and loss.

        Args:
            asset_id (int): Margin asset ID got from get_asset_id() function

        Returns:
            Decimal: The price as Decimal
        """
        self._logger.debug(
            "Trying to get break even price for margin asset with ID:[%s]",
            asset_id,
        )

        # First we get all margin open orders
        all_margin_open_orders: list[dict[str, Any]] = await self.get_all_open_orders()

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

        # If no match found in the server response, raise BreakEvenPriceNotFoundError
        if margin_order is None:
            self._logger.error(
                "Break even price not found for asset ID [%s]!",
                asset_id,
            )

            raise BreakEvenPriceNotFoundError

        # Else, we should have found a result, so we extract the break even price,
        # normalize and return it
        break_even_price: Decimal = await normalize_decimal(
            Decimal(str(margin_order["break_even_point"])),
        )

        self._logger.debug("Break even price found as [%s]", break_even_price)

        return break_even_price

    async def get_margin_pair_id(self, isolated_symbol: str) -> int:
        """Gets the pair ID for a margin asset from server and returns it as an integer.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset.
            example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            int: Margin pair ID an integer
        """
        self._logger.debug(
            "Trying to get margin pair ID of [%s]",
            isolated_symbol,
        )

        # We get the data from server
        isolated_symbol_details: dict[str, Any] = await self._get_isolated_symbol_details(
            isolated_symbol,
        )

        # We extract pair information
        margin_pair_information = isolated_symbol_details["pair"]
        # Then we extract the pair ID and return it
        margin_pair_id: int = margin_pair_information["id"]
        self._logger.debug("Margin pair ID is [%s]", margin_pair_id)

        return margin_pair_id

    async def get_margin_asset_balance(self, isolated_symbol: str) -> Decimal:
        """Gets the margin asset balance in USDT from server and returns it as Decimal value.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset

        Returns:
            Decimal: Asset balance in USDT as Decimal
        """
        self._logger.debug(
            "Trying to get margin asset balance for [%s]",
            isolated_symbol,
        )

        # We get the data from server
        isolated_symbol_details: dict[str, Any] = await self._get_isolated_symbol_details(
            isolated_symbol,
        )

        # We extract margin asset balance
        margin_asset_usdt_details: dict[
            str,
            Any,
        ] = isolated_symbol_details["second_currency_credit"]
        margin_asset_usdt_balance: Decimal = await normalize_decimal(
            Decimal(str(margin_asset_usdt_details["available_amount"])),
        )
        self._logger.debug(
            "Margin asset [%s] balance is [%s]",
            isolated_symbol,
            margin_asset_usdt_balance,
        )

        return margin_asset_usdt_balance

    async def get_margin_asset_precision_requirements(
        self,
        isolated_symbol: str,
    ) -> tuple[int, int]:
        """Gets the precision requirements of an asset from server and returns it as a tuple.

        First return value is precision for volume.
        Seconds return value is precision for price.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset

        Returns:
            tuple[int, int]: A Tuple containing precision requirements for (1)volume and (2)price
        """
        self._logger.debug(
            "Trying to get precision requirements for asset [%s]",
            isolated_symbol,
        )

        # We get the data from server
        isolated_symbol_details: dict[str, Any] = await self._get_isolated_symbol_details(
            isolated_symbol,
        )

        # We extract the precision requirements
        first_currency_details: dict[
            str,
            Any,
        ] = isolated_symbol_details["first_currency_credit"]
        currency_pair_details: dict[str, Any] = first_currency_details["pair"]

        volume_precision: int = currency_pair_details["first_currency_precision"]
        price_precision: int = currency_pair_details["price_precision"]
        self._logger.debug(
            "Precision values for [%s]: Volume -> [%s] | Price -> [%s]",
            isolated_symbol,
            volume_precision,
            price_precision,
        )

        return volume_precision, price_precision

    async def get_margin_asset_trade_able(self, isolated_symbol: str) -> bool:
        """Gets the trade-able status of requested margin asset from server.

        Returns the status as boolean

        Returns false if MarginTradingNotActiveError or MarketNotFoundError

        Args:
            isolated_symbol (str): Isolated symbol of margin asset

        Returns:
            bool: Is margin asset trade-able?
        """
        self._logger.debug(
            "Trying to get trade-able status for [%s]",
            isolated_symbol,
        )

        # We try to get the data from server
        try:
            isolated_symbol_details: dict[str, Any] = await self._get_isolated_symbol_details(
                isolated_symbol,
            )

            # We extract the required variables
            asset_borrow_able: bool = isolated_symbol_details["borrow_active"]
            asset_transfer_able: bool = isolated_symbol_details["transfer_active"]
            asset_trade_able: bool = isolated_symbol_details["active"]

            self._logger.debug(
                "Margin asset [%s] status:\n"
                "Borrow-able -> [%s] | Transfer-able -> [%s] | Trade-able -> [%s]",
                isolated_symbol,
                asset_borrow_able,
                asset_transfer_able,
                asset_trade_able,
            )

        # If market is not found or asset is not available for margin trading
        # We catch the exception and return false
        except (MarketNotFoundError, MarginTradingNotActiveError):
            self._logger.exception(
                "Market not found or asset is not active for margin trading!\nCheck logs",
            )
            return False

        # If everything checks, we return the result
        return asset_borrow_able and asset_transfer_able and asset_trade_able
