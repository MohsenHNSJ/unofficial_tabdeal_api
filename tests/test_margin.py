"""This file is for testing function of margin module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type"
# pylint: disable=W0613,W0612,C0301,W0212

import logging
from typing import TYPE_CHECKING, Any

import pytest
from aiohttp import ClientSession

from tests.test_constants import (
    GET_ALL_MARGIN_OPEN_ORDERS_TEST_RESPONSE_ITEM_COUNT,
    GET_SYMBOL_DETAILS_RESPONSE_DICTIONARY,
    INVALID_ASSET_ID,
    INVALID_ISOLATED_SYMBOL,
    TEST_ASSET_ID,
    TEST_BREAK_EVEN_PRICE,
    TEST_GET_MARGIN_ASSET_DETAILS_URI,
    TEST_ISOLATED_SYMBOL,
    TEST_ISOLATED_SYMBOL_NAME,
    TEST_MARGIN_ASSET_ID,
    TEST_MARGIN_PAIR_ID,
    TEST_SERVER_ADDRESS,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import server_maker
from tests.test_server import server_get_responder
from unofficial_tabdeal_api.constants import GET_ALL_MARGIN_OPEN_ORDERS_URI
from unofficial_tabdeal_api.exceptions import BreakEvenPriceNotFoundError, MarketNotFoundError
from unofficial_tabdeal_api.margin import MarginClass

# Unused imports add a performance overhead at runtime, and risk creating import cycles.
# If an import is only used in typing-only contexts,
# it can instead be imported conditionally under an if TYPE_CHECKING: block to minimize runtime overhead.
if TYPE_CHECKING:  # pragma: no cover
    from decimal import Decimal

    from aiohttp import test_utils


async def test_get_isolated_symbol_details(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the get_isolated_symbol_details function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_get_responder,
        TEST_GET_MARGIN_ASSET_DETAILS_URI,
    )

    # Check correct request
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_get_details: MarginClass = MarginClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        with caplog.at_level(logging.DEBUG):
            response = await test_get_details._get_isolated_symbol_details(TEST_ISOLATED_SYMBOL)
            assert response == GET_SYMBOL_DETAILS_RESPONSE_DICTIONARY
        assert f"Trying to get details of [{TEST_ISOLATED_SYMBOL}]" in caplog.text
        assert (
            f"Details retrieved successfully.\nSymbol name: [{TEST_ISOLATED_SYMBOL_NAME}]"
            in caplog.text
        )

        # Check invalid symbol
        with pytest.raises(MarketNotFoundError):
            response = await test_get_details._get_isolated_symbol_details(INVALID_ISOLATED_SYMBOL)


async def test_get_all_margin_open_orders(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_all_margin_open_orders function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_get_responder,
        GET_ALL_MARGIN_OPEN_ORDERS_URI,
    )

    # Check correct request
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_get_all_object: MarginClass = MarginClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        with caplog.at_level(logging.DEBUG):
            response: list[dict[str, Any]] = await test_get_all_object.get_all_open_orders()
            # Check count of objects
            assert (
                len(
                    response,
                )
                == GET_ALL_MARGIN_OPEN_ORDERS_TEST_RESPONSE_ITEM_COUNT
            )
        # Check debug log is written
        assert "Trying to get all open margin orders" in caplog.text
        assert (
            f"Data retrieved successfully.\nYou have [{GET_ALL_MARGIN_OPEN_ORDERS_TEST_RESPONSE_ITEM_COUNT}] open positions"
            in caplog.text
        )


async def test_get_margin_asset_id(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_margin_asset_id function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_get_responder,
        TEST_GET_MARGIN_ASSET_DETAILS_URI,
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

        with caplog.at_level(logging.DEBUG):
            # Get sample data from server
            response = await test_margin_object.get_margin_asset_id(TEST_ISOLATED_SYMBOL)
            # Check response is okay
            assert response == TEST_MARGIN_ASSET_ID
        assert f"Trying to get asset ID of [{TEST_ISOLATED_SYMBOL}]" in caplog.text
        assert f"Margin asset ID: [{TEST_MARGIN_ASSET_ID}]" in caplog.text


async def test_get_break_even_price(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_break_even_price function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_get_responder,
        GET_ALL_MARGIN_OPEN_ORDERS_URI,
    )

    # Check correct request
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_get_break_even_price_object: MarginClass = MarginClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        # Check correct asset ID
        with caplog.at_level(logging.DEBUG):
            response: Decimal = await test_get_break_even_price_object.get_break_even_price(
                TEST_ASSET_ID,
            )
            # Check response is okay
            assert response == TEST_BREAK_EVEN_PRICE
        # Check log is written
        assert (
            f"Trying to get break even price for margin asset with ID:[{TEST_ASSET_ID}]"
            in caplog.text
        )
        assert f"Break even price found as [{TEST_BREAK_EVEN_PRICE}]" in caplog.text

        # Check wrong asset ID
        with caplog.at_level(logging.ERROR), pytest.raises(BreakEvenPriceNotFoundError):
            wrong_id_response: Decimal = (
                await test_get_break_even_price_object.get_break_even_price(
                    INVALID_ASSET_ID,
                )
            )
        # Check log is written
        assert f"Break even price not found for asset ID [{INVALID_ASSET_ID}]!" in caplog.text


async def test_get_pair_id(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_pair_id function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_get_responder,
        TEST_GET_MARGIN_ASSET_DETAILS_URI,
    )

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_pair_id_object: MarginClass = MarginClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        # Capture logs at level DEBUG and above
        with caplog.at_level(logging.DEBUG):
            # Get sample data from server
            response = await test_pair_id_object.get_pair_id(TEST_ISOLATED_SYMBOL)
            # Check response is okay
            assert response == TEST_MARGIN_PAIR_ID
        # Check logs are written
        assert f"Trying to get pair ID of [{TEST_ISOLATED_SYMBOL}]" in caplog.text
        assert f"Margin pair ID is [{TEST_MARGIN_PAIR_ID}]" in caplog.text
