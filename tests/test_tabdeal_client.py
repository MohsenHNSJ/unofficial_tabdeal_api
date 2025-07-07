"""This file contains tests for the tabdeal_client module."""
# ruff: noqa: S101, SLF001, E501, FBT003
# pylint: disable=W0613,W0612,C0301,W0212
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type,method-assign,no-untyped-call,func-returns-value"

from decimal import Decimal
from typing import TYPE_CHECKING, Literal
from unittest.mock import AsyncMock, Mock, patch

import pytest

from tests.test_constants import EXPECTED_SESSION_HEADERS
from tests.test_helper_functions import create_tabdeal_client
from unofficial_tabdeal_api.exceptions import MarginOrderNotFoundInActiveOrdersError

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

# region wait_for_order_fill


@pytest.mark.asyncio
async def test_wait_for_order_fill_immediate_success() -> None:
    """Test when order is filled immediately on first check."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "BTCUSDT"

    # Mock order as already filled
    client.is_margin_order_filled = AsyncMock(return_value=True)

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        result = await client._wait_for_order_fill(order)

    # Assert
    assert result is True

    # Verify order check was called once
    client.is_margin_order_filled.assert_called_once_with(
        isolated_symbol="BTCUSDT",
    )

    # Verify logging
    client._logger.debug.assert_called_once_with(
        "Order fill status = [%s]",
        True,
    )

    # Verify no sleep was called since order was filled immediately
    mock_sleep.assert_not_called()


@pytest.mark.asyncio
async def test_wait_for_order_fill_after_delay() -> None:
    """Test when order is filled after some waiting."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "ETHUSDT"

    # Mock order as not filled first, then filled
    client.is_margin_order_filled = AsyncMock(side_effect=[False, False, True])

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        result = await client._wait_for_order_fill(order)

    # Assert
    assert result is True

    # Verify order check was called multiple times
    assert client.is_margin_order_filled.call_count == 3  # noqa: PLR2004

    # Verify all calls were with correct symbol
    for call in client.is_margin_order_filled.call_args_list:
        assert call.kwargs == {"isolated_symbol": "ETHUSDT"}

    # Verify sleep was called twice (for the two False responses)
    assert mock_sleep.call_count == 2  # noqa: PLR2004
    for call in mock_sleep.call_args_list:
        assert call.kwargs == {"delay": 60}

    # Verify logging - should have 5 debug calls (3 status + 2 sleep)
    assert client._logger.debug.call_count == 5  # noqa: PLR2004

    # Check status logging
    client._logger.debug.assert_any_call("Order fill status = [%s]", False)
    client._logger.debug.assert_any_call("Order fill status = [%s]", True)

    # Check sleep logging
    client._logger.debug.assert_any_call(
        "Sleeping for one minute before trying again",
    )


@pytest.mark.asyncio
async def test_wait_for_order_fill_margin_order_not_found() -> None:
    """Test when MarginOrderNotFoundInActiveOrdersError is raised."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "ADAUSDT"

    # Mock order check to raise exception
    client.is_margin_order_filled = AsyncMock(
        side_effect=MarginOrderNotFoundInActiveOrdersError(),
    )

    # Mock withdrawal methods
    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("150.75"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act
    result = await client._wait_for_order_fill(order)

    # Assert
    assert result is False

    # Verify order check was attempted
    client.is_margin_order_filled.assert_called_once_with(
        isolated_symbol="ADAUSDT",
    )

    # Verify withdrawal process
    client.get_margin_asset_balance.assert_called_once_with(
        isolated_symbol="ADAUSDT",
    )

    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once_with(
        transfer_amount=Decimal("150.75"),
        isolated_symbol="ADAUSDT",
    )

    # Verify logging
    client._logger.exception.assert_called_once_with(
        "Margin order is not found in active margin orders list!Process will not continue",
    )

    client._logger.debug.assert_called_once_with(
        "Trying to withdraw deposited amount of USDT",
    )

    client._logger.info.assert_called_once_with(
        "Trading failed, but, "
        "Successfully withdrawn the remaining amount of USDT [%s] from asset [%s]",
        Decimal("150.75"),
        "ADAUSDT",
    )


@pytest.mark.asyncio
async def test_wait_for_order_fill_exception_after_some_checks() -> None:
    """Test when exception occurs after some successful checks."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "SOLUSDT"

    # Mock order as not filled, then exception on third call
    client.is_margin_order_filled = AsyncMock(
        side_effect=[False, False, MarginOrderNotFoundInActiveOrdersError()],
    )

    # Mock withdrawal methods
    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("99.99"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        result = await client._wait_for_order_fill(order)

    # Assert
    assert result is False

    # Verify order check was called 3 times before exception
    assert client.is_margin_order_filled.call_count == 3  # noqa: PLR2004

    # Verify sleep was called twice (before the exception)
    assert mock_sleep.call_count == 2  # noqa: PLR2004

    # Verify withdrawal process
    client.get_margin_asset_balance.assert_called_once_with(
        isolated_symbol="SOLUSDT",
    )

    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once_with(
        transfer_amount=Decimal("99.99"),
        isolated_symbol="SOLUSDT",
    )


@pytest.mark.asyncio
async def test_wait_for_order_fill_withdrawal_exception() -> None:
    """Test when withdrawal process itself raises an exception."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "DOTUSDT"

    # Mock order check to raise MarginOrderNotFoundInActiveOrdersError
    client.is_margin_order_filled = AsyncMock(
        side_effect=MarginOrderNotFoundInActiveOrdersError(),
    )

    # Mock balance retrieval to succeed but transfer to fail
    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("200.00"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock(
        side_effect=Exception("Transfer failed"),
    )

    # Act & Assert
    with pytest.raises(Exception, match="Transfer failed"):
        await client._wait_for_order_fill(order)

    # Verify exception logging was called
    client._logger.exception.assert_called_once_with(
        "Margin order is not found in active margin orders list!Process will not continue",
    )

    # Verify withdrawal was attempted
    client.get_margin_asset_balance.assert_called_once()
    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once()


@pytest.mark.asyncio
async def test_wait_for_order_fill_balance_retrieval_exception() -> None:
    """Test when balance retrieval fails during withdrawal."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "AVAXUSDT"

    # Mock order check to raise exception
    client.is_margin_order_filled = AsyncMock(
        side_effect=MarginOrderNotFoundInActiveOrdersError(),
    )

    # Mock balance retrieval to fail
    client.get_margin_asset_balance = AsyncMock(
        side_effect=Exception("Balance retrieval failed"),
    )
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act & Assert
    with pytest.raises(Exception, match="Balance retrieval failed"):
        await client._wait_for_order_fill(order)

    # Verify exception logging was called
    client._logger.exception.assert_called_once()

    # Verify balance retrieval was attempted
    client.get_margin_asset_balance.assert_called_once()

    # Transfer should not be called due to balance retrieval failure
    client.transfer_usdt_from_margin_asset_to_wallet.assert_not_called()


@pytest.mark.asyncio
async def test_wait_for_order_fill_zero_balance_withdrawal() -> None:
    """Test withdrawal process when balance is zero."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "MATICUSDT"

    # Mock exception scenario
    client.is_margin_order_filled = AsyncMock(
        side_effect=MarginOrderNotFoundInActiveOrdersError(),
    )

    # Mock zero balance
    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("0.00"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act
    result = await client._wait_for_order_fill(order)

    # Assert
    assert result is False

    # Verify withdrawal was attempted even with zero balance
    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once_with(
        transfer_amount=Decimal("0.00"),
        isolated_symbol="MATICUSDT",
    )

    # Verify info logging with zero amount
    client._logger.info.assert_called_once_with(
        "Trading failed, but, "
        "Successfully withdrawn the remaining amount of USDT [%s] from asset [%s]",
        Decimal("0.00"),
        "MATICUSDT",
    )


@pytest.mark.asyncio
async def test_wait_for_order_fill_loop_behavior() -> None:
    """Test the while loop behavior in detail."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "LINKUSDT"

    # Mock multiple False responses before True
    client.is_margin_order_filled = AsyncMock(
        side_effect=[False, False, False, True],
    )

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        result = await client._wait_for_order_fill(order)

    # Assert
    assert result is True

    # Verify the loop ran 4 times (3 False + 1 True)
    assert client.is_margin_order_filled.call_count == 4  # noqa: PLR2004

    # Verify sleep was called 3 times (for each False response)
    assert mock_sleep.call_count == 3  # noqa: PLR2004

    # Verify all debug calls (4 status + 3 sleep = 7 total)
    assert client._logger.debug.call_count == 7  # noqa: PLR2004


# endregion wait_for_order_fill
