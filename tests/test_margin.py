"""This file is for testing functions of margin module."""
# ruff: noqa: S101, ANN001, E501, SLF001
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type"
# pylint: disable=W0613,W0612,C0301,W0212

import decimal
import logging
from contextlib import nullcontext
from typing import TYPE_CHECKING, Any

import pytest

from tests.test_constants import (
    GET_ALL_MARGIN_OPEN_ORDERS_SAMPLE_RESPONSE,
    GET_ALL_MARGIN_OPEN_ORDERS_SAMPLE_RESPONSE_SIZE,
    GET_SYMBOL_DETAILS_SAMPLE_RESPONSE,
    INVALID_ASSET_ID,
    INVALID_ISOLATED_SYMBOL,
    INVALID_TYPE_ISOLATED_SYMBOL,
    INVALID_TYPE_TEST_HEADER,
    NOT_AVAILABLE_FOR_MARGIN_SYMBOL,
    SAMPLE_AMOUNT,
    SAMPLE_BREAK_EVEN_PRICE,
    SAMPLE_BUY_BORROWED_USDT_AMOUNT,
    SAMPLE_BUY_BORROWED_VOLUME,
    SAMPLE_BUY_ORDER_VOLUME,
    SAMPLE_BUY_TOTAL_USDT_AMOUNT,
    SAMPLE_ID,
    SAMPLE_MARGIN_ASSET_ID,
    SAMPLE_PRECISION,
    SAMPLE_PRECISION_2,
    SAMPLE_SELL_BORROWED_USDT_AMOUNT,
    SAMPLE_SELL_BORROWED_VOLUME,
    SAMPLE_SELL_ORDER_VOLUME,
    SAMPLE_SELL_TOTAL_USDT_AMOUNT,
    SAMPLE_STOP_LOSS_PRICE,
    SAMPLE_SYMBOL_FULL_NAME,
    SAMPLE_SYMBOL_NAME,
    SAMPLE_SYMBOL_NAME_2,
    SAMPLE_TAKE_PROFIT_PRICE,
    TEST_BUY_MARGIN_LEVEL,
    TEST_BUY_ORDER_ID,
    TEST_BUY_ORDER_OBJECT,
    TEST_SELL_MARGIN_LEVEL,
    TEST_SELL_ORDER_ID,
    TEST_SELL_ORDER_OBJECT,
    TEST_TRUE,
    UN_TRADE_ABLE_SYMBOL,
)
from tests.test_helper_functions import create_tabdeal_client, start_web_server
from unofficial_tabdeal_api.exceptions import (
    BreakEvenPriceNotFoundError,
    MarginOrderNotFoundInActiveOrdersError,
    MarginPositionNotFoundError,
    MarketNotFoundError,
)

# Unused imports add a performance overhead at runtime, and risk creating import cycles.
# If an import is only used in typing-only contexts,
# it can instead be imported conditionally under an if TYPE_CHECKING: block to minimize runtime overhead.
if TYPE_CHECKING:  # pragma: no cover
    from decimal import Decimal

    from unofficial_tabdeal_api.models import IsolatedSymbolDetailsModel, MarginOpenOrderModel
    from unofficial_tabdeal_api.tabdeal_client import TabdealClient

# region TEST-DATA
does_margin_asset_have_active_order_test_data: list[tuple[str, Any]] = [
    (SAMPLE_SYMBOL_NAME, nullcontext(enter_result=True)),
    (
        INVALID_ISOLATED_SYMBOL,
        pytest.raises(
            expected_exception=MarketNotFoundError,
        ),
    ),
]
# endregion TEST-DATA


async def test_get_isolated_symbol_details(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the get_isolated_symbol_details function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Create client session
    test_get_details: TabdealClient = create_tabdeal_client()

    # Check correct request
    with caplog.at_level(level=logging.DEBUG):
        response: IsolatedSymbolDetailsModel = await test_get_details.get_isolated_symbol_details(
            isolated_symbol=SAMPLE_SYMBOL_NAME,
        )
        assert response == GET_SYMBOL_DETAILS_SAMPLE_RESPONSE
    assert f"Trying to get details of [{SAMPLE_SYMBOL_NAME}]" in caplog.text
    assert (
        f"Details retrieved successfully.\nSymbol name: [{SAMPLE_SYMBOL_FULL_NAME}]" in caplog.text
    )

    # Check invalid symbol
    with pytest.raises(expected_exception=MarketNotFoundError):
        await test_get_details.get_isolated_symbol_details(
            isolated_symbol=INVALID_ISOLATED_SYMBOL,
        )

    # Check invalid response type from server
    with caplog.at_level(level=logging.ERROR) and pytest.raises(expected_exception=TypeError):
        await test_get_details.get_isolated_symbol_details(
            isolated_symbol=INVALID_TYPE_ISOLATED_SYMBOL,
        )
    assert "Expected dictionary, got [<class 'list'>]" in caplog.text


async def test_get_all_margin_open_orders(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_all_margin_open_orders function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Check correct request
    test_get_all_object: TabdealClient = create_tabdeal_client()

    # Check correct request
    with caplog.at_level(level=logging.DEBUG):
        response: list[
            MarginOpenOrderModel
        ] = await test_get_all_object.get_margin_all_open_orders()
        # Check count of objects
        assert (
            len(
                response,
            )
            == GET_ALL_MARGIN_OPEN_ORDERS_SAMPLE_RESPONSE_SIZE
        )
        assert response == GET_ALL_MARGIN_OPEN_ORDERS_SAMPLE_RESPONSE
    # Check debug log is written
    assert "Trying to get all open margin orders" in caplog.text
    assert (
        f"Data retrieved successfully.\nYou have [{GET_ALL_MARGIN_OPEN_ORDERS_SAMPLE_RESPONSE_SIZE}] open positions"
        in caplog.text
    )

    # Check invalid response type from server
    with caplog.at_level(level=logging.ERROR) and pytest.raises(expected_exception=TypeError):
        test_get_all_object._client_session.headers.add(
            key=INVALID_TYPE_TEST_HEADER,
            value=TEST_TRUE,
        )
        await test_get_all_object.get_margin_all_open_orders()
    assert "Expected list, got [<class 'dict'>]" in caplog.text


async def test_get_margin_asset_id(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_margin_asset_id function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Check correct request
    # Create an object using test data
    test_margin_object: TabdealClient = create_tabdeal_client()

    with caplog.at_level(level=logging.DEBUG):
        # Get sample data from server
        response = await test_margin_object.get_margin_asset_id(
            isolated_symbol=SAMPLE_SYMBOL_NAME,
        )
        # Check response is okay
        assert response == SAMPLE_ID
    assert f"Trying to get asset ID of [{SAMPLE_SYMBOL_NAME}]" in caplog.text
    assert f"Margin asset ID: [{SAMPLE_ID}]" in caplog.text


async def test_get_order_break_even_price(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_break_even_price function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Check correct request
    test_get_break_even_price_object: TabdealClient = create_tabdeal_client()

    # Check correct asset ID
    with caplog.at_level(level=logging.DEBUG):
        response: Decimal = await test_get_break_even_price_object.get_order_break_even_price(
            asset_id=SAMPLE_ID,
        )
        # Check response is okay
        assert response == SAMPLE_BREAK_EVEN_PRICE
    # Check log is written
    assert f"Trying to get break even price for margin asset with ID:[{SAMPLE_ID}]" in caplog.text
    assert f"Break even price found as [{SAMPLE_BREAK_EVEN_PRICE}]" in caplog.text

    # Check wrong asset ID
    with (
        caplog.at_level(level=logging.ERROR),
        pytest.raises(expected_exception=BreakEvenPriceNotFoundError),
    ):
        (
            await test_get_break_even_price_object.get_order_break_even_price(
                asset_id=INVALID_ASSET_ID,
            )
        )
    # Check log is written
    assert f"Break even price not found for asset ID [{INVALID_ASSET_ID}]!" in caplog.text


async def test_get_margin_pair_id(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_pair_id function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Check correct request
    # Create an object using test data
    test_pair_id_object: TabdealClient = create_tabdeal_client()

    # Capture logs at level DEBUG and above
    with caplog.at_level(level=logging.DEBUG):
        # Get sample data from server
        response: int = await test_pair_id_object.get_margin_pair_id(
            isolated_symbol=SAMPLE_SYMBOL_NAME,
        )
        # Check response is okay
        assert response == SAMPLE_ID
    # Check logs are written
    assert f"Trying to get margin pair ID of [{SAMPLE_SYMBOL_NAME}]" in caplog.text
    assert f"Margin pair ID is [{SAMPLE_ID}]" in caplog.text


async def test_get_margin_asset_balance(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_margin_asset_balance function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Check correct request
    # Create an object using test data
    test_margin_balance_object: TabdealClient = create_tabdeal_client()

    # Capture logs at level DEBUG and above
    with caplog.at_level(level=logging.DEBUG):
        # Get sample data from server
        response: Decimal = await test_margin_balance_object.get_margin_asset_balance(
            isolated_symbol=SAMPLE_SYMBOL_NAME,
        )
        # Check response is okay
        assert response == SAMPLE_AMOUNT
    # Check logs are written
    assert f"Trying to get margin asset balance for [{SAMPLE_SYMBOL_NAME}]" in caplog.text
    assert f"Margin asset [{SAMPLE_SYMBOL_NAME}] balance is [{SAMPLE_AMOUNT}]" in caplog.text


async def test_get_margin_asset_precision_requirements(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the get_margin_asset_precision_requirements function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    test_asset_precision: TabdealClient = create_tabdeal_client()

    # Capture logs at DEBUG and above
    with caplog.at_level(level=logging.DEBUG):
        volume_precision: int
        price_precision: int
        # Get sample data from server
        (
            volume_precision,
            price_precision,
        ) = await test_asset_precision.get_margin_asset_precision_requirements(
            isolated_symbol=SAMPLE_SYMBOL_NAME,
        )
        # Check response is okay
        assert volume_precision == SAMPLE_PRECISION_2
        assert price_precision == SAMPLE_PRECISION
    # Check logs are written
    assert f"Trying to get precision requirements for asset [{SAMPLE_SYMBOL_NAME}]" in caplog.text
    assert (
        f"Precision values for [{SAMPLE_SYMBOL_NAME}]: Volume -> [{SAMPLE_PRECISION_2}] | Price -> [{SAMPLE_PRECISION}]"
        in caplog.text
    )


async def test_get_margin_asset_trade_able(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the get_margin_asset_trade_able function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    test_asset_trade_able: TabdealClient = create_tabdeal_client()

    # Check correct symbol
    # Capture logs at DEBUG and above
    with caplog.at_level(level=logging.DEBUG):
        result: bool = await test_asset_trade_able.is_margin_asset_trade_able(
            isolated_symbol=SAMPLE_SYMBOL_NAME,
        )

        # Check response is okay
        assert result is True
    # Check logs are written
    assert f"Trying to get trade-able status for [{SAMPLE_SYMBOL_NAME}]" in caplog.text
    assert (
        f"Margin asset [{SAMPLE_SYMBOL_NAME}] status:\nBorrow-able -> [True] | Transfer-able -> [True] | Trade-able -> [True]"
        in caplog.text
    )

    # Check un-trade-able symbol
    # Capture logs at DEBUG and above
    with caplog.at_level(level=logging.DEBUG):
        un_trade_able_result: bool = await test_asset_trade_able.is_margin_asset_trade_able(
            isolated_symbol=UN_TRADE_ABLE_SYMBOL,
        )

        # Check response is False
        assert un_trade_able_result is False
    # Check logs are written
    assert (
        f"Margin asset [{UN_TRADE_ABLE_SYMBOL}] status:\nBorrow-able -> [True] | Transfer-able -> [False] | Trade-able -> [True]"
        in caplog.text
    )

    # Check market not found
    with caplog.at_level(level=logging.ERROR):
        market_not_found_result: bool = await test_asset_trade_able.is_margin_asset_trade_able(
            isolated_symbol=INVALID_ISOLATED_SYMBOL,
        )

        # Check response is False
        assert market_not_found_result is False
    # Check logs are written
    assert "Market not found or asset is not active for margin trading!" in caplog.text

    # Check not available for margin trading
    not_available_for_margin_result: bool = await test_asset_trade_able.is_margin_asset_trade_able(
        isolated_symbol=NOT_AVAILABLE_FOR_MARGIN_SYMBOL,
    )
    # Check response is False
    assert not_available_for_margin_result is False


async def test_open_margin_order(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the open_margin_order function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Create client session
    test_open_margin_order_object: TabdealClient = create_tabdeal_client()

    # Check correct BUY request
    with caplog.at_level(level=logging.DEBUG):
        buy_response: int = await test_open_margin_order_object.open_margin_order(
            order=TEST_BUY_ORDER_OBJECT,
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
    with caplog.at_level(level=logging.DEBUG):
        sell_response: int = await test_open_margin_order_object.open_margin_order(
            order=TEST_SELL_ORDER_OBJECT,
        )

        # Check response is okay
        assert sell_response == TEST_SELL_ORDER_ID
    # Check logs are written correctly
    assert (
        f"Trying to open margin order for [{TEST_SELL_ORDER_OBJECT.isolated_symbol}]\nPrice: [{TEST_SELL_ORDER_OBJECT.order_price}] - Amount: [{TEST_SELL_ORDER_OBJECT.deposit_amount}] - Direction: [{TEST_SELL_ORDER_OBJECT.order_side.name}]"
        in caplog.text
    )
    assert (
        f"Order is [{TEST_SELL_ORDER_OBJECT.order_side.name}], margin level set to [{TEST_SELL_MARGIN_LEVEL - decimal.Decimal(value=1)}]"
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
    with caplog.at_level(level=logging.ERROR) and pytest.raises(expected_exception=TypeError):
        # Add invalid type test header to client session
        test_open_margin_order_object._client_session.headers.add(
            key=INVALID_TYPE_TEST_HEADER,
            value=TEST_TRUE,
        )
        # Call the function with invalid object
        await test_open_margin_order_object.open_margin_order(
            order=TEST_BUY_ORDER_OBJECT,
        )
    # Check log is written
    assert "Expected dictionary, got [<class 'list'>]" in caplog.text


async def test_set_sl_tp_for_margin_order(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the set_sl_tp_for_margin_order function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Create client session
    test_set_sl_tp_object: TabdealClient = create_tabdeal_client()

    # Check correct request
    with caplog.at_level(level=logging.DEBUG):
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
    with pytest.raises(expected_exception=MarginPositionNotFoundError):
        await test_set_sl_tp_object.set_sl_tp_for_margin_order(
            margin_asset_id=500,
            stop_loss_price=SAMPLE_STOP_LOSS_PRICE,
            take_profit_price=SAMPLE_TAKE_PROFIT_PRICE,
        )


@pytest.mark.parametrize(
    argnames=("isolated_symbol", "expected_result"),
    argvalues=does_margin_asset_have_active_order_test_data,
)
async def test_does_margin_asset_have_active_order(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
    *,
    isolated_symbol: str,
    expected_result,
) -> None:
    """Tests the does_margin_asset_have_active_order function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Create client session
    test_object: TabdealClient = create_tabdeal_client()

    # Check request
    with caplog.at_level(level=logging.DEBUG), expected_result as e:
        assert (
            await test_object.does_margin_asset_have_active_order(
                isolated_symbol=isolated_symbol,
            )
            == e
        )
    assert f"Checking if [{isolated_symbol}] has active margin order" in caplog.text


async def test_is_margin_order_filled(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the is_margin_order_filled function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Create client session
    test_object: TabdealClient = create_tabdeal_client()

    # Check filled
    with caplog.at_level(level=logging.DEBUG):
        assert await test_object.is_margin_order_filled(SAMPLE_SYMBOL_NAME) is True
    assert (
        f"Checking wether order of margin asset [{SAMPLE_SYMBOL_NAME}] is filled or not"
        in caplog.text
    )

    # Check unfilled
    assert await test_object.is_margin_order_filled(SAMPLE_SYMBOL_NAME_2) is False

    # Check not found
    with pytest.raises(MarginOrderNotFoundInActiveOrdersError):
        await test_object.is_margin_order_filled(UN_TRADE_ABLE_SYMBOL)
