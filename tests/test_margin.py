"""This file is for testing functions of margin module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type"
# pylint: disable=W0613,W0612,C0301,W0212

import decimal
import logging
from typing import TYPE_CHECKING, Any

import pytest
from aiohttp import ClientSession, test_utils

from tests.test_constants import (
    GET_ALL_MARGIN_OPEN_ORDERS_TEST_RESPONSE_ITEM_COUNT,
    GET_SYMBOL_DETAILS_RESPONSE_DICTIONARY,
    INVALID_ASSET_ID,
    INVALID_ISOLATED_SYMBOL,
    INVALID_TYPE_ISOLATED_SYMBOL,
    INVALID_TYPE_TEST_HEADER,
    NOT_AVAILABLE_FOR_MARGIN_SYMBOL,
    SAMPLE_BUY_BORROWED_USDT_AMOUNT,
    SAMPLE_BUY_BORROWED_VOLUME,
    SAMPLE_BUY_ORDER_VOLUME,
    SAMPLE_BUY_TOTAL_USDT_AMOUNT,
    SAMPLE_MARGIN_ASSET_ID,
    SAMPLE_SELL_BORROWED_USDT_AMOUNT,
    SAMPLE_SELL_BORROWED_VOLUME,
    SAMPLE_SELL_ORDER_VOLUME,
    SAMPLE_SELL_TOTAL_USDT_AMOUNT,
    SAMPLE_STOP_LOSS_PRICE,
    SAMPLE_TAKE_PROFIT_PRICE,
    TEST_ASSET_ID,
    TEST_BREAK_EVEN_PRICE,
    TEST_BUY_MARGIN_LEVEL,
    TEST_BUY_ORDER_ID,
    TEST_BUY_ORDER_OBJECT,
    TEST_ISOLATED_SYMBOL,
    TEST_ISOLATED_SYMBOL_NAME,
    TEST_MARGIN_ASSET_BALANCE,
    TEST_MARGIN_ASSET_ID,
    TEST_MARGIN_PAIR_ID,
    TEST_PRICE_PRECISION,
    TEST_SELL_MARGIN_LEVEL,
    TEST_SELL_ORDER_ID,
    TEST_SELL_ORDER_OBJECT,
    TEST_SERVER_ADDRESS,
    TEST_TRUE,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
    TEST_VOLUME_PRECISION,
    UN_TRADE_ABLE_SYMBOL,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import (
    GET_SYMBOL_DETAILS_ENDPOINT,
    OPEN_MARGIN_ORDER_ENDPOINT,
    SET_SL_TP_FOR_MARGIN_ORDER_ENDPOINT,
    enhanced_server_maker,
    server_maker,
)
from tests.test_server import server_get_responder
from unofficial_tabdeal_api.constants import (
    GET_ALL_MARGIN_OPEN_ORDERS_URI,
    GET_MARGIN_ASSET_DETAILS_URI,
)
from unofficial_tabdeal_api.exceptions import (
    BreakEvenPriceNotFoundError,
    MarginPositionNotFoundError,
    MarketNotFoundError,
)
from unofficial_tabdeal_api.margin import MarginClass

# Unused imports add a performance overhead at runtime, and risk creating import cycles.
# If an import is only used in typing-only contexts,
# it can instead be imported conditionally under an if TYPE_CHECKING: block to minimize runtime overhead.
if TYPE_CHECKING:  # pragma: no cover
    from decimal import Decimal


async def test_get_isolated_symbol_details(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the get_isolated_symbol_details function."""
    # Start web server
    server: test_utils.TestServer = await make_test_details_server(aiohttp_server)

    # Create client session
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_get_details: MarginClass = await make_test_margin_object(client_session)

        # Check correct request
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

        # Check invalid response type from server
        with caplog.at_level(logging.ERROR) and pytest.raises(TypeError):
            response = await test_get_details._get_isolated_symbol_details(
                INVALID_TYPE_ISOLATED_SYMBOL,
            )
        assert "Expected dictionary, got [<class 'list'>]" in caplog.text


async def test_get_all_margin_open_orders(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_all_margin_open_orders function."""
    # Start web server
    server: test_utils.TestServer = await make_test_all_orders_server(aiohttp_server)

    # Check correct request
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_get_all_object: MarginClass = await make_test_margin_object(client_session)

        # Check correct request
        with caplog.at_level(logging.DEBUG):
            response: list[dict[str, Any]] = await test_get_all_object.get_margin_all_open_orders()
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

        # Check invalid response type from server
        with caplog.at_level(logging.ERROR) and pytest.raises(TypeError):
            client_session.headers.add(INVALID_TYPE_TEST_HEADER, TEST_TRUE)
            invalid_object: MarginClass = await make_test_margin_object(client_session)
            response = await invalid_object.get_margin_all_open_orders()
        assert "Expected list, got [<class 'dict'>]" in caplog.text


async def test_get_margin_asset_id(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_margin_asset_id function."""
    # Start web server
    server: test_utils.TestServer = await make_test_details_server(aiohttp_server)

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_margin_object: MarginClass = await make_test_margin_object(client_session)

        with caplog.at_level(logging.DEBUG):
            # Get sample data from server
            response = await test_margin_object.get_margin_asset_id(TEST_ISOLATED_SYMBOL)
            # Check response is okay
            assert response == TEST_MARGIN_ASSET_ID
        assert f"Trying to get asset ID of [{TEST_ISOLATED_SYMBOL}]" in caplog.text
        assert f"Margin asset ID: [{TEST_MARGIN_ASSET_ID}]" in caplog.text


async def test_get_order_break_even_price(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_break_even_price function."""
    # Start web server
    server: test_utils.TestServer = await make_test_all_orders_server(aiohttp_server)

    # Check correct request
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_get_break_even_price_object: MarginClass = await make_test_margin_object(
            client_session,
        )

        # Check correct asset ID
        with caplog.at_level(logging.DEBUG):
            response: Decimal = await test_get_break_even_price_object.get_order_break_even_price(
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
                await test_get_break_even_price_object.get_order_break_even_price(
                    INVALID_ASSET_ID,
                )
            )
        # Check log is written
        assert f"Break even price not found for asset ID [{INVALID_ASSET_ID}]!" in caplog.text


async def test_get_margin_pair_id(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_pair_id function."""
    # Start web server
    server: test_utils.TestServer = await make_test_details_server(aiohttp_server)

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_pair_id_object: MarginClass = await make_test_margin_object(client_session)

        # Capture logs at level DEBUG and above
        with caplog.at_level(logging.DEBUG):
            # Get sample data from server
            response: int = await test_pair_id_object.get_margin_pair_id(TEST_ISOLATED_SYMBOL)
            # Check response is okay
            assert response == TEST_MARGIN_PAIR_ID
        # Check logs are written
        assert f"Trying to get margin pair ID of [{TEST_ISOLATED_SYMBOL}]" in caplog.text
        assert f"Margin pair ID is [{TEST_MARGIN_PAIR_ID}]" in caplog.text


async def test_get_margin_asset_balance(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_margin_asset_balance function."""
    # Start web server
    server: test_utils.TestServer = await make_test_details_server(aiohttp_server)

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_margin_balance_object: MarginClass = await make_test_margin_object(client_session)

        # Capture logs at level DEBUG and above
        with caplog.at_level(logging.DEBUG):
            # Get sample data from server
            response: Decimal = await test_margin_balance_object.get_margin_asset_balance(
                TEST_ISOLATED_SYMBOL,
            )
            # Check response is okay
            assert response == TEST_MARGIN_ASSET_BALANCE
        # Check logs are written
        assert f"Trying to get margin asset balance for [{TEST_ISOLATED_SYMBOL}]" in caplog.text
        assert (
            f"Margin asset [{TEST_ISOLATED_SYMBOL}] balance is [{TEST_MARGIN_ASSET_BALANCE}]"
            in caplog.text
        )


async def test_get_margin_asset_precision_requirements(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the get_margin_asset_precision_requirements function."""
    # Start web server
    server: test_utils.TestServer = await make_test_details_server(aiohttp_server)

    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_asset_precision: MarginClass = await make_test_margin_object(client_session)

        # Capture logs at DEBUG and above
        with caplog.at_level(logging.DEBUG):
            volume_precision: int
            price_precision: int
            # Get sample data from server
            (
                volume_precision,
                price_precision,
            ) = await test_asset_precision.get_margin_asset_precision_requirements(
                TEST_ISOLATED_SYMBOL,
            )
            # Check response is okay
            assert volume_precision == TEST_VOLUME_PRECISION
            assert price_precision == TEST_PRICE_PRECISION
        # Check logs are written
        assert (
            f"Trying to get precision requirements for asset [{TEST_ISOLATED_SYMBOL}]"
            in caplog.text
        )
        assert (
            f"Precision values for [{TEST_ISOLATED_SYMBOL}]: Volume -> [{TEST_VOLUME_PRECISION}] | Price -> [{TEST_PRICE_PRECISION}]"
            in caplog.text
        )


async def test_get_margin_asset_trade_able(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the get_margin_asset_trade_able function."""
    # Start web server
    server: test_utils.TestServer = await make_test_details_server(aiohttp_server)

    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_asset_trade_able: MarginClass = await make_test_margin_object(client_session)

        # Check correct symbol
        # Capture logs at DEBUG and above
        with caplog.at_level(logging.DEBUG):
            result: bool = await test_asset_trade_able.get_margin_asset_trade_able(
                TEST_ISOLATED_SYMBOL,
            )

            # Check response is okay
            assert result is True
        # Check logs are written
        assert f"Trying to get trade-able status for [{TEST_ISOLATED_SYMBOL}]" in caplog.text
        assert (
            f"Margin asset [{TEST_ISOLATED_SYMBOL}] status:\nBorrow-able -> [True] | Transfer-able -> [True] | Trade-able -> [True]"
            in caplog.text
        )

        # Check un-trade-able symbol
        # Capture logs at DEBUG and above
        with caplog.at_level(logging.DEBUG):
            un_trade_able_result: bool = await test_asset_trade_able.get_margin_asset_trade_able(
                UN_TRADE_ABLE_SYMBOL,
            )

            # Check response is False
            assert un_trade_able_result is False
        # Check logs are written
        assert (
            f"Margin asset [{UN_TRADE_ABLE_SYMBOL}] status:\nBorrow-able -> [True] | Transfer-able -> [False] | Trade-able -> [True]"
            in caplog.text
        )

        # Check market not found
        with caplog.at_level(logging.ERROR):
            market_not_found_result: bool = await test_asset_trade_able.get_margin_asset_trade_able(
                INVALID_ISOLATED_SYMBOL,
            )

            # Check response is False
            assert market_not_found_result is False
        # Check logs are written
        assert "Market not found or asset is not active for margin trading!" in caplog.text

        # Check not available for margin trading
        not_available_for_margin_result: bool = (
            await test_asset_trade_able.get_margin_asset_trade_able(NOT_AVAILABLE_FOR_MARGIN_SYMBOL)
        )
        # Check response is False
        assert not_available_for_margin_result is False


async def test_open_margin_order(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the open_margin_order function."""
    # Start web server
    server: test_utils.TestServer = await make_test_open_order_server(aiohttp_server)

    # Create client session
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_open_margin_order_object: MarginClass = await make_test_margin_object(client_session)

        # Check correct BUY request
        with caplog.at_level(logging.DEBUG):
            buy_response: int = await test_open_margin_order_object.open_margin_order(
                TEST_BUY_ORDER_OBJECT,
            )

            # Check response is okay
            assert buy_response == TEST_BUY_ORDER_ID
        # Check logs are written correctly
        assert (
            f"Trying to open margin order for [{TEST_BUY_ORDER_OBJECT.isolated_symbol}]\nPrice: [{TEST_BUY_ORDER_OBJECT.order_price}] - Amount: [{TEST_BUY_ORDER_OBJECT.deposit_amount}] - Direction: [{TEST_BUY_ORDER_OBJECT.order_side.name}]"
            in caplog.text
        )
        assert (
            f"Order is [{TEST_BUY_ORDER_OBJECT.order_side.name}], margin level set to [{TEST_BUY_MARGIN_LEVEL}]"
            in caplog.text
        )
        assert (
            f"Total USDT amount: [{SAMPLE_BUY_TOTAL_USDT_AMOUNT}] - Borrowed USDT: [{SAMPLE_BUY_BORROWED_USDT_AMOUNT}]"
            in caplog.text
        )
        assert (
            f"Order volume: [{SAMPLE_BUY_ORDER_VOLUME}] - Borrowed volume: [{SAMPLE_BUY_BORROWED_VOLUME}]"
            in caplog.text
        )
        assert (
            f"Order is [{TEST_BUY_ORDER_OBJECT.order_side.name}]. Borrow quantity set to [{SAMPLE_BUY_BORROWED_USDT_AMOUNT}]"
            in caplog.text
        )
        assert (
            f"Order placed successfully!\nOrder ID: [{TEST_BUY_ORDER_ID}]\nOrder State: [FILLED]"
            in caplog.text
        )

        # Check correct SELL request
        with caplog.at_level(logging.DEBUG):
            sell_response: int = await test_open_margin_order_object.open_margin_order(
                TEST_SELL_ORDER_OBJECT,
            )

            # Check response is okay
            assert sell_response == TEST_SELL_ORDER_ID
        # Check logs are written correctly
        assert (
            f"Trying to open margin order for [{TEST_SELL_ORDER_OBJECT.isolated_symbol}]\nPrice: [{TEST_SELL_ORDER_OBJECT.order_price}] - Amount: [{TEST_SELL_ORDER_OBJECT.deposit_amount}] - Direction: [{TEST_SELL_ORDER_OBJECT.order_side.name}]"
            in caplog.text
        )
        assert (
            f"Order is [{TEST_SELL_ORDER_OBJECT.order_side.name}], margin level set to [{TEST_SELL_MARGIN_LEVEL - decimal.Decimal(1)}]"
            in caplog.text
        )
        assert (
            f"Total USDT amount: [{SAMPLE_SELL_TOTAL_USDT_AMOUNT}] - Borrowed USDT: [{SAMPLE_SELL_BORROWED_USDT_AMOUNT}]"
            in caplog.text
        )
        assert (
            f"Order volume: [{SAMPLE_SELL_ORDER_VOLUME}] - Borrowed volume: [{SAMPLE_SELL_BORROWED_VOLUME}]"
            in caplog.text
        )
        assert (
            f"Order is [{TEST_SELL_ORDER_OBJECT.order_side.name}]. Borrow quantity set to [{SAMPLE_SELL_ORDER_VOLUME}]"
            in caplog.text
        )
        assert (
            f"Order placed successfully!\nOrder ID: [{TEST_SELL_ORDER_ID}]\nOrder State: [PENDING]"
            in caplog.text
        )

        # Check invalid type response
        with caplog.at_level(logging.ERROR) and pytest.raises(TypeError):
            # Add invalid type test header to client session
            client_session.headers.add(INVALID_TYPE_TEST_HEADER, TEST_TRUE)
            # Create an invalid object
            invalid_object: MarginClass = await make_test_margin_object(client_session)
            # Call the function with invalid object
            invalid_response = await test_open_margin_order_object.open_margin_order(
                TEST_BUY_ORDER_OBJECT,
            )
        # Check log is written
        assert "Expected dictionary, got [<class 'list'>]" in caplog.text


async def test_set_sl_tp_for_margin_order(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the set_sl_tp_for_margin_order function."""
    # Start web server
    server: test_utils.TestServer = await make_test_sl_tp_server(aiohttp_server)

    # Create client session
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_set_sl_tp_object: MarginClass = await make_test_margin_object(client_session)

        # Check correct request
        with caplog.at_level(logging.DEBUG):
            await test_set_sl_tp_object.set_sl_tp_for_margin_order(
                margin_asset_id=SAMPLE_MARGIN_ASSET_ID,
                stop_loss_price=SAMPLE_STOP_LOSS_PRICE,
                take_profit_price=SAMPLE_TAKE_PROFIT_PRICE,
            )
        assert (
            f"Trying to set SL [{SAMPLE_STOP_LOSS_PRICE}] and TP [{SAMPLE_TAKE_PROFIT_PRICE}] for margin asset with ID [{SAMPLE_MARGIN_ASSET_ID}]"
            in caplog.text
        )
        assert (
            f"Stop loss [{SAMPLE_STOP_LOSS_PRICE}] and take profit [{SAMPLE_TAKE_PROFIT_PRICE}] has been set for margin asset with ID [{SAMPLE_MARGIN_ASSET_ID}]"
            in caplog.text
        )

        # Check invalid request
        with pytest.raises(MarginPositionNotFoundError):
            await test_set_sl_tp_object.set_sl_tp_for_margin_order(
                margin_asset_id=500,
                stop_loss_price=SAMPLE_STOP_LOSS_PRICE,
                take_profit_price=SAMPLE_TAKE_PROFIT_PRICE,
            )


async def make_test_margin_object(client_session: ClientSession) -> MarginClass:
    """Creates a test object for testing MarginClass."""
    return MarginClass(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
        client_session=client_session,
    )


async def make_test_details_server(aiohttp_server) -> test_utils.TestServer:
    """Creates the server for testing MarginClass."""
    return await server_maker(
        aiohttp_server=aiohttp_server,
        http_request_method=HttpRequestMethod.GET,
        function_to_call=server_get_responder,
        uri_path=GET_MARGIN_ASSET_DETAILS_URI,
    )


async def make_test_all_orders_server(aiohttp_server) -> test_utils.TestServer:
    """Creates the server for testing MarginClass."""
    return await server_maker(
        aiohttp_server=aiohttp_server,
        http_request_method=HttpRequestMethod.GET,
        function_to_call=server_get_responder,
        uri_path=GET_ALL_MARGIN_OPEN_ORDERS_URI,
    )


async def make_test_open_order_server(aiohttp_server) -> test_utils.TestServer:
    """Creates the server for testing MarginClass."""
    return await enhanced_server_maker(
        aiohttp_server=aiohttp_server,
        endpoints=[OPEN_MARGIN_ORDER_ENDPOINT, GET_SYMBOL_DETAILS_ENDPOINT],
    )


async def make_test_sl_tp_server(aiohttp_server) -> test_utils.TestServer:
    """Creates the server for testing SL/TP setting."""
    return await enhanced_server_maker(
        aiohttp_server=aiohttp_server,
        endpoints=[SET_SL_TP_FOR_MARGIN_ORDER_ENDPOINT],
    )
