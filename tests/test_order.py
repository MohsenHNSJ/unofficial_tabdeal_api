"""This file is for testing functions of order module."""
# ruff: noqa: S101, ANN001, F841, E501, SLF001
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type"
# pylint: disable=W0613,W0612,C0301,W0212

import logging
from decimal import Decimal
from typing import TYPE_CHECKING, Any

import pytest

from tests.test_constants import (
    FIRST_SAMPLE_ORDER_PRICE,
    INVALID_TYPE_TEST_HEADER,
    SAMPLE_GET_ORDERS_HISTORY_LIST,
    SAMPLE_INVALID_ORDER_ID,
    SAMPLE_MARGIN_LEVEL,
    SAMPLE_MAX_HISTORY,
    SAMPLE_ORDER_ID,
    SAMPLE_ORDERS_LIST_ITEMS_COUNT,
    TEST_ISOLATED_SYMBOL,
    TEST_MARGIN_ASSET_BALANCE,
    TEST_TRUE,
    TEST_VOLUME_PRECISION,
)
from tests.test_helper_functions import create_tabdeal_client, start_web_server
from unofficial_tabdeal_api.enums import OrderSide, OrderState
from unofficial_tabdeal_api.exceptions import (
    OrderNotFoundInSpecifiedHistoryRangeError,
    RequestedParametersInvalidError,
)
from unofficial_tabdeal_api.order import MarginOrder

if TYPE_CHECKING:  # pragma: no cover
    from unofficial_tabdeal_api.tabdeal_client import TabdealClient


async def test_order_object() -> None:
    """Tests the initialization of order object."""
    # Create the test object
    test_order: MarginOrder = MarginOrder(
        isolated_symbol=TEST_ISOLATED_SYMBOL,
        order_price=FIRST_SAMPLE_ORDER_PRICE,
        order_side=OrderSide.BUY,
        margin_level=SAMPLE_MARGIN_LEVEL,
        deposit_amount=TEST_MARGIN_ASSET_BALANCE,
        stop_loss_percent=Decimal(5),
        take_profit_percent=Decimal(5),
        volume_fraction_allowed=True,
        volume_precision=TEST_VOLUME_PRECISION,
    )

    # Check if fields are set correctly
    assert test_order.isolated_symbol == TEST_ISOLATED_SYMBOL
    assert test_order.order_price == FIRST_SAMPLE_ORDER_PRICE
    assert test_order.order_side == OrderSide.BUY
    assert test_order.margin_level == SAMPLE_MARGIN_LEVEL
    assert test_order.deposit_amount == TEST_MARGIN_ASSET_BALANCE
    assert test_order.volume_fraction_allowed is True
    assert test_order.volume_precision == TEST_VOLUME_PRECISION


async def test_get_orders_details_history(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the _get_orders_details_history function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    test_order: TabdealClient = await create_tabdeal_client()

    # Check correct request
    with caplog.at_level(level=logging.DEBUG):
        response: list[dict[str, Any]] = await test_order.get_orders_details_history(
            max_history=SAMPLE_MAX_HISTORY,
        )
        assert response == SAMPLE_GET_ORDERS_HISTORY_LIST
    assert f"Trying to get last [{SAMPLE_MAX_HISTORY}] orders details" in caplog.text
    assert f"Retrieved [{SAMPLE_ORDERS_LIST_ITEMS_COUNT}] orders history" in caplog.text

    # Check invalid request
    with pytest.raises(expected_exception=RequestedParametersInvalidError):
        await test_order.get_orders_details_history(
            max_history=7,
        )

    # Check invalid type response
    # Add test header to return invalid type
    test_order._client_session.headers.add(
        key=INVALID_TYPE_TEST_HEADER,
        value=TEST_TRUE,
    )
    # Create invalid type object
    with caplog.at_level(level=logging.ERROR) and pytest.raises(expected_exception=TypeError):
        # Check response
        await test_order.get_orders_details_history()
    assert "Expected dictionary, got [<class 'list'>]" in caplog.text


async def test_get_order_state(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_order_state function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Create client session
    test_get_order_status: TabdealClient = await create_tabdeal_client()

    # Check correct request
    with caplog.at_level(level=logging.DEBUG):
        response: OrderState = await test_get_order_status.get_order_state(
            order_id=SAMPLE_ORDER_ID,
        )
        assert response is OrderState.FILLED
    assert f"Getting order state for [{SAMPLE_ORDER_ID}]" in caplog.text
    assert f"Order [{SAMPLE_ORDER_ID}] is in [{response.name}] state" in caplog.text

    # Check invalid request
    with caplog.at_level(level=logging.ERROR) and pytest.raises(
        expected_exception=OrderNotFoundInSpecifiedHistoryRangeError,
    ):
        await test_get_order_status.get_order_state(
            SAMPLE_INVALID_ORDER_ID,
        )
    assert f"Order [{SAMPLE_INVALID_ORDER_ID}] is not found! Check order ID" in caplog.text
