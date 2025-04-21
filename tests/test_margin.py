"""This file is for testing function of margin module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable"
# pylint: disable=W0613,W0612,C0301

import logging
from typing import Any

import pytest
from aiohttp import ClientSession, test_utils, web

from tests.test_constants import (
    GET_ALL_MARGIN_OPEN_ORDERS_TEST_RESPONSE_ITEM_COUNT,
    INVALID_SERVER_ADDRESS,
    INVALID_USER_AUTH_KEY,
    INVALID_USER_HASH,
    STATUS_BAD_REQUEST,
    TEST_GET_ALL_MARGIN_OPEN_ORDERS_CONTENT,
    TEST_GET_ALL_MARGIN_OPEN_ORDERS_URI,
    TEST_GET_MARGIN_ASSET_ID,
    TEST_ISOLATED_MARGIN_MARKET_GENRE,
    TEST_ISOLATED_SYMBOL,
    TEST_MARGIN_ASSET_ID,
    TEST_SERVER_ADDRESS,
    TEST_URI_FAILED_CONTENT,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import server_maker
from unofficial_tabdeal_api.margin import MarginClass


async def test_get_margin_asset_id(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_margin_asset_id function."""
    # Create the URI
    get_margin_asset_details_uri: str = "/margin/margin-account-v2/"

    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_margin_asset_id_responder,
        get_margin_asset_details_uri,
    )

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_margin_object: MarginClass = MarginClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        # Get sample data from server
        response = await test_margin_object.get_margin_asset_id(TEST_ISOLATED_SYMBOL)
        # Check response is okay
        assert response == TEST_MARGIN_ASSET_ID

    # Check error
    # Create an aiohttp.ClientSession object with base url set to invalid address
    async with ClientSession(base_url=INVALID_SERVER_ADDRESS) as client_session:
        # Create an invalid object
        error_margin_object: MarginClass = MarginClass(
            INVALID_USER_HASH,
            INVALID_USER_AUTH_KEY,
            client_session,
        )

        # Capture logs at level ERROR and above
        with caplog.at_level(logging.ERROR):
            # Get the error message
            response = await error_margin_object.get_margin_asset_id(TEST_ISOLATED_SYMBOL)
            # Check response is -1
            assert response == -1
        # Check error is written to log
        assert "Failed to get margin asset ID for" in caplog.text


async def test_get_all_margin_open_orders(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_all_margin_open_orders function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_get_all_margin_open_orders_responder,
        TEST_GET_ALL_MARGIN_OPEN_ORDERS_URI,
    )

    # Check correct request
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_get_all_object: MarginClass = MarginClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        with caplog.at_level(logging.DEBUG):
            response: (
                list[dict[str, Any]] | None
            ) = await test_get_all_object.get_all_open_margin_orders()
            # Check count of objects
            if response is not None:
                assert (
                    len(
                        response,
                    )
                    == GET_ALL_MARGIN_OPEN_ORDERS_TEST_RESPONSE_ITEM_COUNT
                )
        # Check debug log is written
        assert "Trying to get all open margin orders" in caplog.text
        assert "List of all open margin orders has [2] items" in caplog.text

    # Check error
    async with ClientSession(base_url=INVALID_SERVER_ADDRESS) as client_session:
        invalid_get_all_object: MarginClass = MarginClass(
            INVALID_USER_HASH,
            INVALID_USER_AUTH_KEY,
            client_session,
        )

        with caplog.at_level(logging.ERROR):
            invalid_response: (
                list[dict[str, Any]] | None
            ) = await invalid_get_all_object.get_all_open_margin_orders()
            # Check response is None
            assert invalid_response is None
        # Check error is written to log
        assert (
            "Failed to get all open margin orders! Returning server response: [None]" in caplog.text
        )


async def server_margin_asset_id_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server for checking margin asset ID."""
    # Check request query
    pair_symbol: str | None = request.query.get("pair_symbol")
    account_genre: str | None = request.query.get("account_genre")
    if (pair_symbol == TEST_ISOLATED_SYMBOL) and (
        account_genre == TEST_ISOLATED_MARGIN_MARKET_GENRE
    ):
        return web.Response(text=TEST_GET_MARGIN_ASSET_ID)

    return web.Response(text=TEST_URI_FAILED_CONTENT, status=STATUS_BAD_REQUEST)


async def server_get_all_margin_open_orders_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server for checking get all margin open orders."""
    # Return data as success
    return web.Response(text=TEST_GET_ALL_MARGIN_OPEN_ORDERS_CONTENT)
