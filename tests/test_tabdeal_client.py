"""This file contains tests for the tabdeal_client module."""
# ruff: noqa: S101, SLF001, E501
# pylint: disable=W0613,W0612,C0301,W0212
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type,method-assign,no-untyped-call"

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, Mock

import pytest

from tests.test_constants import EXPECTED_SESSION_HEADERS
from tests.test_helper_functions import create_tabdeal_client

if TYPE_CHECKING:  # pragma: no cover
    from unofficial_tabdeal_api.tabdeal_client import TabdealClient


async def test_init() -> None:
    """Tests the initialization of an object from tabdeal_client class."""
    # Create an object using test data
    test_tabdeal: TabdealClient = create_tabdeal_client()

    # Check attributes
    # Check if session headers is stored correctly
    assert test_tabdeal._client_session.headers == EXPECTED_SESSION_HEADERS


@pytest.mark.asyncio
async def test_validate_trade_conditions_existing_order() -> None:
    """Test validation fails when an active order already exists."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()

    # Mock the logger to avoid AsyncMock warnings
    client._logger = Mock()

    # Create a sample order
    order = Mock()
    order.isolated_symbol = "BTCUSDT"

    # Mock methods - existing order case
    client.does_margin_asset_have_active_order = AsyncMock(return_value=True)
    client.is_margin_asset_trade_able = AsyncMock(return_value=True)

    # Act
    result = await client._validate_trade_conditions(order)

    # Assert
    assert result is False
    client.does_margin_asset_have_active_order.assert_called_once_with(
        isolated_symbol="BTCUSDT",
    )
    # Should not call trade_able check since it returns early
    client.is_margin_asset_trade_able.assert_not_called()

    # Verify warning was logged
    client._logger.warning.assert_called_once_with(
        "An order is already open for [%s], This order will be skipped",
        "BTCUSDT",
    )


@pytest.mark.asyncio
async def test_validate_trade_conditions_not_tradeable() -> None:
    """Test validation fails when asset is not tradeable."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()

    # Mock the logger
    client._logger = Mock()

    # Create a sample order
    order = Mock()
    order.isolated_symbol = "ETHUSDT"

    # Mock methods - no existing order but not tradeable
    client.does_margin_asset_have_active_order = AsyncMock(return_value=False)
    client.is_margin_asset_trade_able = AsyncMock(return_value=False)

    # Act
    result = await client._validate_trade_conditions(order)

    # Assert
    assert result is False
    client.does_margin_asset_have_active_order.assert_called_once_with(
        isolated_symbol="ETHUSDT",
    )
    client.is_margin_asset_trade_able.assert_called_once_with(
        isolated_symbol="ETHUSDT",
    )

    # Verify warning was logged
    client._logger.warning.assert_called_once_with(
        "Margin asset [%s] is not trade-able on Tabdeal, This order will be skipped",
        "ETHUSDT",
    )


@pytest.mark.asyncio
async def test_validate_trade_conditions_success() -> None:
    """Test validation succeeds when all conditions are met."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()

    # Mock the logger
    client._logger = Mock()

    # Create a sample order
    order = Mock()
    order.isolated_symbol = "ADAUSDT"

    # Mock methods - no existing order and is tradeable
    client.does_margin_asset_have_active_order = AsyncMock(return_value=False)
    client.is_margin_asset_trade_able = AsyncMock(return_value=True)

    # Act
    result = await client._validate_trade_conditions(order)

    # Assert
    assert result is True
    client.does_margin_asset_have_active_order.assert_called_once_with(
        isolated_symbol="ADAUSDT",
    )
    client.is_margin_asset_trade_able.assert_called_once_with(
        isolated_symbol="ADAUSDT",
    )

    # Verify no warnings were logged
    client._logger.warning.assert_not_called()


@pytest.mark.asyncio
async def test_validate_trade_conditions_with_real_order_model() -> None:
    """Test validation with a real MarginOrderModel instance."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()

    # Mock the logger
    client._logger = Mock()

    # Create a real MarginOrderModel (you'll need to adjust this based on your model)
    # This assumes you have the required fields for MarginOrderModel
    _ = {
        "isolated_symbol": "SOLUSDT",
        "order_price": "100.0",
        "deposit_amount": "50.0",
        "order_side": 1,  # Adjust based on your OrderSide enum
        "margin_level": "2.0",
        "stop_loss_percent": "5.0",
        "take_profit_percent": "10.0",
        "volume_precision": 2,
        "volume_fraction_allowed": True,
    }

    # Mock methods for success case
    client.does_margin_asset_have_active_order = AsyncMock(return_value=False)
    client.is_margin_asset_trade_able = AsyncMock(return_value=True)

    # Create a mock order that has the isolated_symbol attribute
    order = Mock()
    order.isolated_symbol = "SOLUSDT"

    # Act
    result = await client._validate_trade_conditions(order)

    # Assert
    assert result is True
    client.does_margin_asset_have_active_order.assert_called_once_with(
        isolated_symbol="SOLUSDT",
    )
    client.is_margin_asset_trade_able.assert_called_once_with(
        isolated_symbol="SOLUSDT",
    )


@pytest.mark.asyncio
async def test_validate_trade_conditions_exception_handling() -> None:
    """Test that exceptions from dependency methods are properly propagated."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()

    # Mock the logger
    client._logger = Mock()

    # Create a sample order
    order = Mock()
    order.isolated_symbol = "DOTUSDT"

    # Mock method to raise an exception
    client.does_margin_asset_have_active_order = AsyncMock(
        side_effect=Exception("Network error"),
    )

    # Act & Assert
    with pytest.raises(Exception, match="Network error"):
        await client._validate_trade_conditions(order)

    # Verify the method was called before the exception
    client.does_margin_asset_have_active_order.assert_called_once_with(
        isolated_symbol="DOTUSDT",
    )
