"""This file is for testing functions of order module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type"
# pylint: disable=W0613,W0612,C0301,W0212

import logging
from typing import Any

import pytest
from aiohttp import ClientSession, test_utils

from tests.test_constants import (
    SAMPLE_GET_ORDERS_HISTORY_LIST,
    SAMPLE_MAX_HISTORY,
    SAMPLE_ORDER_ID,
    SAMPLE_ORDERS_LIST_ITEMS_COUNT,
    TEST_SERVER_ADDRESS,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import server_maker
from tests.test_server import server_get_responder
from unofficial_tabdeal_api.constants import GET_ORDERS_HISTORY_URI
from unofficial_tabdeal_api.enums import OrderState
from unofficial_tabdeal_api.order import OrderClass


async def test_get_orders_details_history(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the _get_orders_details_history function."""
    # Start web server
    server: test_utils.TestServer = await make_test_order_server(aiohttp_server)

    # Check correct request
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_get_orders: OrderClass = await make_test_order_object(client_session)

        with caplog.at_level(logging.DEBUG):
            response: list[dict[str, Any]] = await test_get_orders._get_orders_details_history(
                SAMPLE_MAX_HISTORY,
            )
            assert response == SAMPLE_GET_ORDERS_HISTORY_LIST
        assert f"Trying to get last [{SAMPLE_MAX_HISTORY}] orders details" in caplog.text
        assert f"Retrieved [{SAMPLE_ORDERS_LIST_ITEMS_COUNT}] orders history" in caplog.text


async def test_get_order_state(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_order_state function."""
    # Start web server
    server: test_utils.TestServer = await make_test_order_server(aiohttp_server)

    # Check correct request
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_get_order_status: OrderClass = await make_test_order_object(client_session)

        with caplog.at_level(logging.DEBUG):
            response: OrderState = await test_get_order_status.get_order_state(SAMPLE_ORDER_ID)
            assert response is OrderState.FILLED
        assert f"Getting order state for [{SAMPLE_ORDER_ID}]" in caplog.text
        assert f"Order [{SAMPLE_ORDER_ID}] is in [{response.name}] state" in caplog.text


async def make_test_order_server(aiohttp_server) -> test_utils.TestServer:
    """Creates the server for testing OrderClass."""
    return await server_maker(
        aiohttp_server=aiohttp_server,
        http_request_method=HttpRequestMethod.GET,
        function_to_call=server_get_responder,
        uri_path=GET_ORDERS_HISTORY_URI,
    )


async def make_test_order_object(client_session: ClientSession) -> OrderClass:
    """Creates a test object for testing OrderClass."""
    return OrderClass(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
        client_session=client_session,
    )
