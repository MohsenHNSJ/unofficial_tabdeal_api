"""This module holds the OrderClass."""
# pylint: disable=R0913

from decimal import Decimal
from typing import Any

from pydantic import BaseModel

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import GET_ORDERS_HISTORY_URI
from unofficial_tabdeal_api.enums import OrderSide, OrderState
from unofficial_tabdeal_api.exceptions import OrderNotFoundInSpecifiedHistoryRangeError


class MarginOrder(BaseModel):
    """This is the class storing information about a margin order."""

    isolated_symbol: str
    """Symbol of the order, e.g. BTCUSDT"""
    order_price: Decimal
    """Price of the order, e.g. 10000.00"""
    order_side: OrderSide
    """Side of the order, either BUY or SELL"""
    margin_level: Decimal
    """Margin level of the order, e.g. 1.5"""
    deposit_amount: Decimal
    """Deposit amount for the order, e.g. 1000.00"""
    stop_loss_percent: Decimal
    """Percentile of tolerate-able loss, e.g. 5 for 5%"""
    take_profit_percent: Decimal
    """Percentile of expected profit, e.g. 10 for 10%"""
    volume_fraction_allowed: bool
    """Whether volume fraction is allowed, e.g. True or False"""
    volume_precision: int = 0
    """Precision of the volume, Defaults to 0"""


class OrderClass(BaseClass):
    """This is the class storing methods related to Ordering."""

    async def get_orders_details_history(self, max_history: int = 500) -> list[dict[str, Any]]:
        """Gets the last 500(by default) orders details and returns them as a list.

        Args:
            max_history (int, optional): Max number of histories. Defaults to 500.

        Raises:
            TypeError: If the server responds incorrectly

        Returns:
            list[dict[str, Any]]: A List of dictionaries
        """
        self._logger.debug(
            "Trying to get last [%s] orders details",
            max_history,
        )

        # We create the connection query
        connection_query: dict[str, Any] = {
            "page_size": max_history,
            "ordering": "created",
            "desc": "true",
            "market_type": "All",
            "order_type": "All",
        }

        # We get the data from server
        response = await self._get_data_from_server(
            connection_url=GET_ORDERS_HISTORY_URI,
            queries=connection_query,
        )

        # If the type is correct, we process, log and return the data
        if isinstance(response, dict):
            list_of_orders: list[dict[str, Any]] = response["orders"]

            self._logger.debug(
                "Retrieved [%s] orders history",
                len(list_of_orders),
            )

            return list_of_orders

        # Else, we log and raise TypeError
        self._logger.error("Expected dictionary, got [%s]", type(response))

        raise TypeError

    async def get_order_state(self, order_id: int) -> OrderState:
        """Gets the state of the requested order and returns it as an OrderState enum.

        Args:
            order_id (int): ID of the trade order

        Returns:
            OrderState: State of the order as enum
        """
        self._logger.debug("Getting order state for [%s]", order_id)

        # We get the list of last orders history
        orders_history: list[dict[str, Any]] = await self.get_orders_details_history()

        # Then we search through the list and find the order ID we are looking for
        # And store that into our variable
        # Get the first object in the list that meets a condition, if nothing found, return [None]
        order_details: dict[str, Any] | None = next(
            (order for order in orders_history if order["id"] == order_id),
            None,
        )

        # If no match found in the server response, raise OrderNotFoundInSpecifiedHistoryRange
        if order_details is None:
            self._logger.error(
                "Order [%s] is not found! Check order ID",
                order_id,
            )

            raise OrderNotFoundInSpecifiedHistoryRangeError

        # Else, we should have found a result, so we extract the order state
        # and return it
        order_state: OrderState = OrderState(order_details["state"])

        self._logger.debug(
            "Order [%s] is in [%s] state",
            order_id,
            order_state.name,
        )

        return order_state
