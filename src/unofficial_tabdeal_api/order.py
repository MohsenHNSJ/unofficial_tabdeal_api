"""This module holds the OrderClass."""

from typing import Any

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import GET_ORDERS_HISTORY_URI


class OrderClass(BaseClass):
    """This is the class storing methods related to Ordering."""

    async def _get_orders_details_history(self, max_history: int = 500) -> list[dict[str, Any]]:
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


# {
#     "orders": [
#         {
#             "created": "2025-05-11T15:07:30.974347+03:30",
#             "updated": "2025-05-11T15:07:31.152964+03:30",
#             "id": 6275274104,
#             "trader_id": 383698,
#             "market_id": 861,
#             "market_type": 3,
#             "first_currency_account_credit_id": 43009535,
#             "second_currency_account_credit_id": 43009536,
#             "side": 1,
#             "order_type": 1,
#             "state": 4,
#             "source": 2,
#             "amount": 556.0,
#             "price": 0.002157,
#             "is_part_of_oco": false,
#             "stop_order_limit": false,
#             "comment": null,
#             "need_to_call_webhook": false,
#             "filled_amount": 556.0,
#             "average_price": 0.002157,
#             "non_market_maker_filled_amount": null,
#             "new_non_mm_filled_amount": 0.0,
#             "new_non_mm_avg_price": null,
#             "non_mm_fields_last_updated": null,
#             "show": true,
#             "core": 2,
#             "status": 3,
#             "active": false,
#             "order_moved": false,
#             "kafka_valid": null,
#             "kafka_cancel_valid": true,
#             "state_valid": null,
#             "user_device_id": 4761260,
#             "user_device_cancel_id": null,
#             "db_cancel_time": null,
#             "core_cancel_time": null,
#             "order_identifier_id": null,
#             "market_name": "بوک اف میم_تتر",
#             "market_name_link": "BOME_USDT"
#         },
#     ]
# }
