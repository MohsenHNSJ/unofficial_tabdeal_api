"""This file contains tests for the tabdeal_client module."""
# ruff: noqa: S101, SLF001, E501
# pylint: disable=W0613,W0612,C0301,W0212
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type,method-assign,no-untyped-call"

from collections.abc import Generator
from decimal import Decimal
from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pytest

from tests.test_constants import EXPECTED_SESSION_HEADERS
from tests.test_helper_functions import create_tabdeal_client
from unofficial_tabdeal_api.enums import OrderSide
from unofficial_tabdeal_api.exceptions import MarginOrderNotFoundInActiveOrdersError
from unofficial_tabdeal_api.models import MarginOrderModel
from unofficial_tabdeal_api.tabdeal_client import TabdealClient


async def test_init() -> None:
    """Tests the initialization of an object from tabdeal_client class."""
    # Create an object using test data
    test_tabdeal: TabdealClient = create_tabdeal_client()

    # Check attributes
    # Check if session headers is stored correctly
    assert test_tabdeal._client_session.headers == EXPECTED_SESSION_HEADERS


@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
async def test_trade_margin_order(mock_sleep) -> None:  # noqa: ANN001, ARG001
    """Test all code paths of trade_margin_order."""
    client = TabdealClient(
        user_hash="test",
        authorization_key="test",
        _is_test=True,
    )
    # Patch logger to AsyncMock for call assertions
    logger_mock = Mock()
    client._logger = logger_mock
    order = MarginOrderModel(
        isolated_symbol="TESTUSDT",
        order_price=Decimal("1.0"),
        order_side=OrderSide.BUY,
        margin_level=Decimal("2.0"),
        deposit_amount=Decimal("10.0"),
        stop_loss_percent=Decimal("5.0"),
        take_profit_percent=Decimal("10.0"),
        volume_fraction_allowed=True,
        volume_precision=2,
    )

    # 1. Already has active order
    client.does_margin_asset_have_active_order = AsyncMock(return_value=True)
    client.is_margin_asset_trade_able = AsyncMock()
    result: bool = await client.trade_margin_order(order=order, withdraw_balance_after_trade=False)
    assert result is False
    logger_mock.warning.assert_called_with(
        "An order is already open for [%s], This order will be skipped",
        order.isolated_symbol,
    )

    # 2. Not tradeable
    client.does_margin_asset_have_active_order = AsyncMock(return_value=False)
    client.is_margin_asset_trade_able = AsyncMock(return_value=False)
    result = await client.trade_margin_order(order=order, withdraw_balance_after_trade=False)
    assert result is False
    logger_mock.warning.assert_called_with(
        "Margin asset [%s] is not trade-able on Tabdeal, This order will be skipped",
        order.isolated_symbol,
    )

    # 3. Normal successful trade
    client.does_margin_asset_have_active_order = AsyncMock(return_value=False)
    client.is_margin_asset_trade_able = AsyncMock(return_value=True)
    client.transfer_usdt_from_wallet_to_margin_asset = AsyncMock()
    client.open_margin_order = AsyncMock(return_value=123)
    client.is_margin_order_filled = AsyncMock(side_effect=[False, True])
    client.get_margin_asset_id = AsyncMock(return_value=123)
    client.get_order_break_even_price = AsyncMock(return_value=Decimal("1.5"))
    client.get_margin_asset_precision_requirements = AsyncMock(
        return_value=(None, 0),
    )
    client.set_sl_tp_for_margin_order = AsyncMock()
    # Simulate order closes after one loop

    def close_order_side_effect() -> Generator[list[dict[str, int]], Any, None]:
        yield [{"id": 123}]
        yield []

    client.get_margin_all_open_orders = AsyncMock(
        side_effect=close_order_side_effect(),
    )
    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("5.0"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()
    result = await client.trade_margin_order(order=order, withdraw_balance_after_trade=True)
    assert result is True
    logger_mock.debug.assert_any_call("Trade finished")
    logger_mock.debug.assert_any_call(
        "User asked to withdraw balance after trade",
    )
    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_with(
        transfer_amount=Decimal("5.0"),
        isolated_symbol=order.isolated_symbol,
    )

    # 4. MarginOrderNotFoundInActiveOrdersError path
    client.is_margin_order_filled = AsyncMock(
        side_effect=MarginOrderNotFoundInActiveOrdersError,
    )
    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("7.0"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()
    result = await client.trade_margin_order(order=order, withdraw_balance_after_trade=False)
    assert result is False
    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_with(
        transfer_amount=Decimal("7.0"),
        isolated_symbol=order.isolated_symbol,
    )
    logger_mock.info.assert_any_call(
        "Trading failed, but, "
        "Successfully withdrawn the remaining amount of USDT [%s] from asset [%s]",
        Decimal("7.0"),
        order.isolated_symbol,
    )
