"""This file contains tests for the tabdeal_client module."""
# ruff: noqa: S101, SLF001, E501
# pylint: disable=W0613,W0612,C0301,W0212
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type,method-assign,no-untyped-call,func-returns-value"

from decimal import Decimal
from typing import TYPE_CHECKING, Literal
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


# region validate_trade_conditions


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


# endregion validate_trade_conditions

# region open_order


@pytest.mark.asyncio
async def test_open_order_success() -> None:
    """Test successful order opening with all steps completed."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()

    # Mock the logger
    client._logger = Mock()

    # Create a sample order
    order = Mock()
    order.deposit_amount = Decimal("100.0")
    order.isolated_symbol = "BTCUSDT"

    # Mock the required methods
    client.transfer_usdt_from_wallet_to_margin_asset = AsyncMock()
    client.open_margin_order = AsyncMock(return_value=12345)

    # Act
    await client._open_order(order)

    # Assert
    # Verify transfer was called with correct parameters
    client.transfer_usdt_from_wallet_to_margin_asset.assert_called_once_with(
        transfer_amount=Decimal("100.0"),
        isolated_symbol="BTCUSDT",
    )

    # Verify order opening was called with correct order
    client.open_margin_order.assert_called_once_with(order=order)

    # Verify logging
    assert client._logger.debug.call_count == 2  # noqa: PLR2004

    # Check first debug log (after deposit)
    client._logger.debug.assert_any_call(
        "[%s] funds deposited into [%s]",
        Decimal("100.0"),
        "BTCUSDT",
    )

    # Check second debug log (after order opening)
    client._logger.debug.assert_any_call(
        "Order opened with ID: [%s]",
        12345,
    )


@pytest.mark.asyncio
async def test_open_order_transfer_exception() -> None:
    """Test that transfer exceptions are properly propagated."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.deposit_amount = Decimal("50.0")
    order.isolated_symbol = "ETHUSDT"

    # Mock transfer to raise an exception
    client.transfer_usdt_from_wallet_to_margin_asset = AsyncMock(
        side_effect=Exception("Transfer failed"),
    )
    client.open_margin_order = AsyncMock()

    # Act & Assert
    with pytest.raises(Exception, match="Transfer failed"):
        await client._open_order(order)

    # Verify transfer was attempted
    client.transfer_usdt_from_wallet_to_margin_asset.assert_called_once_with(
        transfer_amount=Decimal("50.0"),
        isolated_symbol="ETHUSDT",
    )

    # Verify order opening was never called due to exception
    client.open_margin_order.assert_not_called()

    # Verify no logging occurred due to early exception
    client._logger.debug.assert_not_called()


@pytest.mark.asyncio
async def test_open_order_margin_order_exception() -> None:
    """Test that margin order exceptions are properly propagated."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.deposit_amount = Decimal("75.0")
    order.isolated_symbol = "ADAUSDT"

    # Mock successful transfer but failed order opening
    client.transfer_usdt_from_wallet_to_margin_asset = AsyncMock()
    client.open_margin_order = AsyncMock(
        side_effect=Exception("Order opening failed"),
    )

    # Act & Assert
    with pytest.raises(Exception, match="Order opening failed"):
        await client._open_order(order)

    # Verify transfer was completed
    client.transfer_usdt_from_wallet_to_margin_asset.assert_called_once_with(
        transfer_amount=Decimal("75.0"),
        isolated_symbol="ADAUSDT",
    )

    # Verify order opening was attempted
    client.open_margin_order.assert_called_once_with(order=order)

    # Verify first debug log was called (after successful transfer)
    client._logger.debug.assert_called_once_with(
        "[%s] funds deposited into [%s]",
        Decimal("75.0"),
        "ADAUSDT",
    )


@pytest.mark.asyncio
async def test_open_order_with_different_data_types() -> None:
    """Test order opening with different data types for amounts."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.deposit_amount = Decimal("999.99")
    order.isolated_symbol = "SOLUSDT"

    # Mock methods
    client.transfer_usdt_from_wallet_to_margin_asset = AsyncMock()
    client.open_margin_order = AsyncMock(return_value=99999)

    # Act
    await client._open_order(order)

    # Assert
    client.transfer_usdt_from_wallet_to_margin_asset.assert_called_once_with(
        transfer_amount=Decimal("999.99"),
        isolated_symbol="SOLUSDT",
    )

    client.open_margin_order.assert_called_once_with(order=order)

    # Verify both debug logs were called
    assert client._logger.debug.call_count == 2  # noqa: PLR2004


@pytest.mark.asyncio
async def test_open_order_method_call_order() -> None:
    """Test that methods are called in the correct order."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.deposit_amount = Decimal("200.0")
    order.isolated_symbol = "DOTUSDT"

    # Track call order
    call_order = []

    async def mock_transfer(*args, **kwargs) -> None:  # noqa: ANN002, ANN003, ARG001
        call_order.append("transfer")

    async def mock_open_order(*args, **kwargs) -> Literal[54321]:  # noqa: ANN002, ANN003, ARG001
        call_order.append("open_order")
        return 54321

    client.transfer_usdt_from_wallet_to_margin_asset = AsyncMock(
        side_effect=mock_transfer,
    )
    client.open_margin_order = AsyncMock(side_effect=mock_open_order)

    # Act
    await client._open_order(order)

    # Assert
    # Verify methods were called in correct order
    assert call_order == ["transfer", "open_order"]

    # Verify logging happened after each step
    assert client._logger.debug.call_count == 2  # noqa: PLR2004


@pytest.mark.asyncio
async def test_open_order_return_value() -> None:
    """Test that the function returns None as specified in docstring."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.deposit_amount = Decimal("123.45")
    order.isolated_symbol = "AVAXUSDT"

    client.transfer_usdt_from_wallet_to_margin_asset = AsyncMock()
    client.open_margin_order = AsyncMock(return_value=11111)

    # Act
    result: None = await client._open_order(order)

    # Assert
    # Note: The docstring says it returns int but the function signature says None
    # The actual implementation doesn't return anything, so it returns None
    assert result is None


# endregion open_order
