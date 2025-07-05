"""This module holds the OrderClass."""
# pylint: disable=R0913

from typing import Any

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import GET_ORDERS_HISTORY_URI
from unofficial_tabdeal_api.enums import OrderState
from unofficial_tabdeal_api.exceptions import OrderNotFoundInSpecifiedHistoryRangeError
from unofficial_tabdeal_api.utils import find_order_by_id


class OrderClass(BaseClass):
    """This is the class storing methods related to Ordering."""

    async def get_orders_details_history(self, _max_history: int = 500) -> list[dict[str, Any]]:
        """Gets the last 500(by default) orders details and returns them as a list.

        Args:
            _max_history (int, optional): Max number of histories. Defaults to 500.

        Raises:
            TypeError: If the server responds incorrectly

        Returns:
            list[dict[str, Any]]: A List of dictionaries
        """
        self._logger.debug(
            "Trying to get last [%s] orders details",
            _max_history,
        )

        # We create the connection query
        connection_query: dict[str, Any] = {
            "page_size": _max_history,
            "ordering": "created",
            "desc": "true",
            "market_type": "All",
            "order_type": "All",
        }

        # We get the data from server
        response: dict[str, Any] | list[dict[str, Any]] = await self._get_data_from_server(
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
        order_details: dict[str, Any] | None = find_order_by_id(
            orders_list=orders_history,
            order_id=order_id,
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
