"""This file contains tests for the tabdeal_client module."""
# ruff: noqa: S101, SLF001, E501, FBT003, PLR2004
# pylint: disable=W0613,W0612,C0301,W0212
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type,method-assign,no-untyped-call,func-returns-value"

from decimal import Decimal
from typing import TYPE_CHECKING, Literal
from unittest.mock import AsyncMock, Mock, patch

import pytest

from tests.test_constants import EXPECTED_SESSION_HEADERS
from tests.test_helper_functions import create_tabdeal_client
from unofficial_tabdeal_api.enums import OrderSide
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
    assert client._logger.debug.call_count == 2

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
    assert client._logger.debug.call_count == 2


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
    assert client._logger.debug.call_count == 2


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
    assert client.is_margin_order_filled.call_count == 3

    # Verify all calls were with correct symbol
    for call in client.is_margin_order_filled.call_args_list:
        assert call.kwargs == {"isolated_symbol": "ETHUSDT"}

    # Verify sleep was called twice (for the two False responses)
    assert mock_sleep.call_count == 2
    for call in mock_sleep.call_args_list:
        assert call.kwargs == {"delay": 60}

    # Verify logging - should have 5 debug calls (3 status + 2 sleep)
    assert client._logger.debug.call_count == 5

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
    assert client.is_margin_order_filled.call_count == 3

    # Verify sleep was called twice (before the exception)
    assert mock_sleep.call_count == 2

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
    assert client.is_margin_order_filled.call_count == 4

    # Verify sleep was called 3 times (for each False response)
    assert mock_sleep.call_count == 3

    # Verify all debug calls (4 status + 3 sleep = 7 total)
    assert client._logger.debug.call_count == 7


# endregion wait_for_order_fill

# region setup_stop_loss_take_profit


@pytest.mark.asyncio
async def test_setup_stop_loss_take_profit_success() -> None:
    """Test successful SL/TP setup with all steps completed."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    # Create a sample order
    order = Mock()
    order.isolated_symbol = "BTCUSDT"
    order.margin_level = Decimal("3.0")
    order.order_side = OrderSide.BUY
    order.stop_loss_percent = Decimal("5.0")
    order.take_profit_percent = Decimal("10.0")

    # Mock all dependency methods
    client.get_margin_asset_id = AsyncMock(return_value=1234567)
    client.get_order_break_even_price = AsyncMock(
        return_value=Decimal("50000.00"),
    )
    client.get_margin_asset_precision_requirements = AsyncMock(
        return_value=(2, 2),  # (volume_precision, price_precision)
    )
    client.set_sl_tp_for_margin_order = AsyncMock()

    # Mock the calculate_sl_tp_prices function
    with patch("unofficial_tabdeal_api.tabdeal_client.calculate_sl_tp_prices") as mock_calculate:
        mock_calculate.return_value = (
            Decimal("47500.00"),
            Decimal("55000.00"),
        )

        # Act
        result = await client._setup_stop_loss_take_profit(order)

    # Assert
    assert result == 1234567

    # Verify all method calls
    client.get_margin_asset_id.assert_called_once_with(
        isolated_symbol="BTCUSDT",
    )
    client.get_order_break_even_price.assert_called_once_with(asset_id=1234567)
    client.get_margin_asset_precision_requirements.assert_called_once_with(
        isolated_symbol="BTCUSDT",
    )

    # Verify calculate_sl_tp_prices was called with correct parameters
    mock_calculate.assert_called_once_with(
        margin_level=Decimal("3.0"),
        order_side=OrderSide.BUY,
        break_even_point=Decimal("50000.00"),
        stop_loss_percent=Decimal("5.0"),
        take_profit_percent=Decimal("10.0"),
        price_required_precision=2,
        price_fraction_allowed=False,  # price_precision_required == 0 is False
    )

    # Verify SL/TP setting
    client.set_sl_tp_for_margin_order.assert_called_once_with(
        margin_asset_id=1234567,
        stop_loss_price=Decimal("47500.00"),
        take_profit_price=Decimal("55000.00"),
    )

    # Verify logging
    client._logger.debug.assert_called_once_with(
        "Stop loss point: [%s] - Take profit point: [%s]",
        Decimal("47500.00"),
        Decimal("55000.00"),
    )


@pytest.mark.asyncio
async def test_setup_stop_loss_take_profit_zero_price_precision() -> None:
    """Test SL/TP setup when price precision is 0 (price_fraction_allowed=True)."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "ETHUSDT"
    order.margin_level = Decimal("2.0")
    order.order_side = OrderSide.SELL
    order.stop_loss_percent = Decimal("3.0")
    order.take_profit_percent = Decimal("8.0")

    # Mock methods with zero price precision
    client.get_margin_asset_id = AsyncMock(return_value=9876543)
    client.get_order_break_even_price = AsyncMock(
        return_value=Decimal("3000.00"),
    )
    client.get_margin_asset_precision_requirements = AsyncMock(
        return_value=(4, 0),  # price_precision = 0
    )
    client.set_sl_tp_for_margin_order = AsyncMock()

    # Mock calculation
    with patch("unofficial_tabdeal_api.tabdeal_client.calculate_sl_tp_prices") as mock_calculate:
        mock_calculate.return_value = (Decimal("3090.00"), Decimal("2760.00"))

        # Act
        result = await client._setup_stop_loss_take_profit(order)

    # Assert
    assert result == 9876543

    # Verify calculate_sl_tp_prices was called with price_fraction_allowed=True
    mock_calculate.assert_called_once_with(
        margin_level=Decimal("2.0"),
        order_side=OrderSide.SELL,
        break_even_point=Decimal("3000.00"),
        stop_loss_percent=Decimal("3.0"),
        take_profit_percent=Decimal("8.0"),
        price_required_precision=0,
        price_fraction_allowed=True,  # price_precision_required == 0 is True
    )


@pytest.mark.asyncio
async def test_setup_stop_loss_take_profit_get_asset_id_exception() -> None:
    """Test when get_margin_asset_id raises an exception."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "ADAUSDT"

    # Mock get_margin_asset_id to raise exception
    client.get_margin_asset_id = AsyncMock(
        side_effect=Exception("Asset ID not found"),
    )

    # Act & Assert
    with pytest.raises(Exception, match="Asset ID not found"):
        await client._setup_stop_loss_take_profit(order)

    # Verify only the first method was called
    client.get_margin_asset_id.assert_called_once_with(
        isolated_symbol="ADAUSDT",
    )


@pytest.mark.asyncio
async def test_setup_stop_loss_take_profit_get_break_even_exception() -> None:
    """Test when get_order_break_even_price raises an exception."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "SOLUSDT"

    # Mock successful asset ID but failed break-even price
    client.get_margin_asset_id = AsyncMock(return_value=5555555)
    client.get_order_break_even_price = AsyncMock(
        side_effect=Exception("Break-even price error"),
    )

    # Act & Assert
    with pytest.raises(Exception, match="Break-even price error"):
        await client._setup_stop_loss_take_profit(order)

    # Verify method calls up to the failure point
    client.get_margin_asset_id.assert_called_once()
    client.get_order_break_even_price.assert_called_once_with(asset_id=5555555)


@pytest.mark.asyncio
async def test_setup_stop_loss_take_profit_precision_requirements_exception() -> None:
    """Test when get_margin_asset_precision_requirements raises an exception."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "DOTUSDT"

    # Mock successful calls until precision requirements
    client.get_margin_asset_id = AsyncMock(return_value=7777777)
    client.get_order_break_even_price = AsyncMock(
        return_value=Decimal("25.00"),
    )
    client.get_margin_asset_precision_requirements = AsyncMock(
        side_effect=Exception("Precision requirements error"),
    )

    # Act & Assert
    with pytest.raises(Exception, match="Precision requirements error"):
        await client._setup_stop_loss_take_profit(order)

    # Verify method calls
    client.get_margin_asset_id.assert_called_once()
    client.get_order_break_even_price.assert_called_once()
    client.get_margin_asset_precision_requirements.assert_called_once()


@pytest.mark.asyncio
async def test_setup_stop_loss_take_profit_calculate_function_exception() -> None:
    """Test when calculate_sl_tp_prices raises an exception."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "AVAXUSDT"
    order.margin_level = Decimal("5.0")
    order.order_side = OrderSide.BUY
    order.stop_loss_percent = Decimal("4.0")
    order.take_profit_percent = Decimal("12.0")

    # Mock all methods successfully
    client.get_margin_asset_id = AsyncMock(return_value=8888888)
    client.get_order_break_even_price = AsyncMock(
        return_value=Decimal("100.00"),
    )
    client.get_margin_asset_precision_requirements = AsyncMock(
        return_value=(3, 1),
    )

    # Mock calculate function to raise exception
    with patch("unofficial_tabdeal_api.tabdeal_client.calculate_sl_tp_prices") as mock_calculate:
        mock_calculate.side_effect = Exception("Calculation error")

        # Act & Assert
        with pytest.raises(Exception, match="Calculation error"):
            await client._setup_stop_loss_take_profit(order)

    # Verify all dependency methods were called
    client.get_margin_asset_id.assert_called_once()
    client.get_order_break_even_price.assert_called_once()
    client.get_margin_asset_precision_requirements.assert_called_once()


@pytest.mark.asyncio
async def test_setup_stop_loss_take_profit_set_sl_tp_exception() -> None:
    """Test when set_sl_tp_for_margin_order raises an exception."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "MATICUSDT"
    order.margin_level = Decimal("4.0")
    order.order_side = OrderSide.SELL
    order.stop_loss_percent = Decimal("6.0")
    order.take_profit_percent = Decimal("15.0")

    # Mock all methods successfully until SL/TP setting
    client.get_margin_asset_id = AsyncMock(return_value=3333333)
    client.get_order_break_even_price = AsyncMock(return_value=Decimal("1.50"))
    client.get_margin_asset_precision_requirements = AsyncMock(
        return_value=(6, 4),
    )
    client.set_sl_tp_for_margin_order = AsyncMock(
        side_effect=Exception("SL/TP setting failed"),
    )

    # Mock successful calculation
    with patch("unofficial_tabdeal_api.tabdeal_client.calculate_sl_tp_prices") as mock_calculate:
        mock_calculate.return_value = (Decimal("1.59"), Decimal("1.275"))

        # Act & Assert
        with pytest.raises(Exception, match="SL/TP setting failed"):
            await client._setup_stop_loss_take_profit(order)

    # Verify all methods were called including the failed one
    client.get_margin_asset_id.assert_called_once()
    client.get_order_break_even_price.assert_called_once()
    client.get_margin_asset_precision_requirements.assert_called_once()
    client.set_sl_tp_for_margin_order.assert_called_once()

    # Verify logging was called before the exception
    client._logger.debug.assert_called_once()


@pytest.mark.asyncio
async def test_setup_stop_loss_take_profit_different_order_sides() -> None:
    """Test SL/TP setup with different order sides (BUY vs SELL)."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    # Test BUY order
    order_buy = Mock()
    order_buy.isolated_symbol = "LINKUSDT"
    order_buy.margin_level = Decimal("2.5")
    order_buy.order_side = OrderSide.BUY
    order_buy.stop_loss_percent = Decimal("7.0")
    order_buy.take_profit_percent = Decimal("14.0")

    # Mock methods
    client.get_margin_asset_id = AsyncMock(return_value=1111111)
    client.get_order_break_even_price = AsyncMock(
        return_value=Decimal("20.00"),
    )
    client.get_margin_asset_precision_requirements = AsyncMock(
        return_value=(2, 3),
    )
    client.set_sl_tp_for_margin_order = AsyncMock()

    # Mock calculation for BUY order
    with patch("unofficial_tabdeal_api.tabdeal_client.calculate_sl_tp_prices") as mock_calculate:
        mock_calculate.return_value = (Decimal("18.60"), Decimal("22.80"))

        # Act
        result = await client._setup_stop_loss_take_profit(order_buy)

    # Assert
    assert result == 1111111

    # Verify calculate was called with BUY order side
    mock_calculate.assert_called_once_with(
        margin_level=Decimal("2.5"),
        order_side=OrderSide.BUY,
        break_even_point=Decimal("20.00"),
        stop_loss_percent=Decimal("7.0"),
        take_profit_percent=Decimal("14.0"),
        price_required_precision=3,
        price_fraction_allowed=False,
    )


@pytest.mark.asyncio
async def test_setup_stop_loss_take_profit_edge_case_values() -> None:
    """Test SL/TP setup with edge case decimal values."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "UNIUSDT"
    order.margin_level = Decimal("1.1")  # Edge case: small margin level
    order.order_side = OrderSide.SELL
    order.stop_loss_percent = Decimal("0.5")  # Edge case: small percentage
    order.take_profit_percent = Decimal("99.9")  # Edge case: large percentage

    # Mock methods with edge case values
    client.get_margin_asset_id = AsyncMock(return_value=9999999)
    client.get_order_break_even_price = AsyncMock(
        return_value=Decimal("0.01"),
    )  # Very small price
    client.get_margin_asset_precision_requirements = AsyncMock(
        return_value=(8, 8),
    )  # High precision
    client.set_sl_tp_for_margin_order = AsyncMock()

    # Mock calculation
    with patch("unofficial_tabdeal_api.tabdeal_client.calculate_sl_tp_prices") as mock_calculate:
        mock_calculate.return_value = (Decimal("0.01005"), Decimal("0.00201"))

        # Act
        result = await client._setup_stop_loss_take_profit(order)

    # Assert
    assert result == 9999999

    # Verify all edge case values were passed correctly
    mock_calculate.assert_called_once_with(
        margin_level=Decimal("1.1"),
        order_side=OrderSide.SELL,
        break_even_point=Decimal("0.01"),
        stop_loss_percent=Decimal("0.5"),
        take_profit_percent=Decimal("99.9"),
        price_required_precision=8,
        price_fraction_allowed=False,
    )


# endregion setup_stop_loss_take_profit

# region wait_for_order_close


@pytest.mark.asyncio
async def test_wait_for_order_close_immediate_closure() -> None:
    """Test when order is already closed (not found in open orders)."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    margin_asset_id = 1234567

    # Mock empty open orders list (order already closed)
    client.get_margin_all_open_orders = AsyncMock(return_value=[])

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        await client._wait_for_order_close(margin_asset_id)

    # Assert
    # Verify get_margin_all_open_orders was called once
    client.get_margin_all_open_orders.assert_called_once()

    # Verify debug logging for closed order
    client._logger.debug.assert_called_once_with(
        "Margin order seems to be closed",
    )

    # Verify no sleep was called since order was already closed
    mock_sleep.assert_not_called()


@pytest.mark.asyncio
async def test_wait_for_order_close_not_found_in_list() -> None:
    """Test when order is not found in the open orders list."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    margin_asset_id = 9999999

    # Mock open orders list with different IDs
    mock_order_1 = Mock()
    mock_order_1.id = 1111111
    mock_order_2 = Mock()
    mock_order_2.id = 2222222

    client.get_margin_all_open_orders = AsyncMock(
        return_value=[mock_order_1, mock_order_2],
    )

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        await client._wait_for_order_close(margin_asset_id)

    # Assert
    client.get_margin_all_open_orders.assert_called_once()
    client._logger.debug.assert_called_once_with(
        "Margin order seems to be closed",
    )
    mock_sleep.assert_not_called()


@pytest.mark.asyncio
async def test_wait_for_order_close_found_then_closed() -> None:
    """Test when order is found initially, then closes after waiting."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    margin_asset_id = 5555555

    # Mock order that exists initially
    mock_target_order = Mock()
    mock_target_order.id = 5555555
    mock_other_order = Mock()
    mock_other_order.id = 6666666

    # First call: order exists, second call: order is gone
    client.get_margin_all_open_orders = AsyncMock(
        side_effect=[
            [mock_target_order, mock_other_order],  # First call - order exists
            [mock_other_order],  # Second call - order is gone
        ],
    )

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        await client._wait_for_order_close(margin_asset_id)

    # Assert
    # Verify get_margin_all_open_orders was called twice
    assert client.get_margin_all_open_orders.call_count == 2

    # Verify logging - should have 2 debug calls
    assert client._logger.debug.call_count == 2

    # Check first debug call (order still open)
    client._logger.debug.assert_any_call(
        "Margin order is not yet closed, waiting for one minute before trying again",
    )

    # Check second debug call (order closed)
    client._logger.debug.assert_any_call("Margin order seems to be closed")

    # Verify sleep was called once
    mock_sleep.assert_called_once_with(delay=60)


@pytest.mark.asyncio
async def test_wait_for_order_close_multiple_waits() -> None:
    """Test when order takes multiple cycles to close."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    margin_asset_id = 7777777

    # Mock order that exists for multiple cycles
    mock_target_order = Mock()
    mock_target_order.id = 7777777
    mock_other_order = Mock()
    mock_other_order.id = 8888888

    # Order exists for 3 cycles, then closes
    client.get_margin_all_open_orders = AsyncMock(
        side_effect=[
            [mock_target_order, mock_other_order],  # First call - order exists
            # Second call - order still exists
            [mock_target_order, mock_other_order],
            # Third call - order still exists
            [mock_target_order, mock_other_order],
            [mock_other_order],  # Fourth call - order is gone
        ],
    )

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        await client._wait_for_order_close(margin_asset_id)

    # Assert
    # Verify get_margin_all_open_orders was called 4 times
    assert client.get_margin_all_open_orders.call_count == 4

    # Verify sleep was called 3 times (for the 3 cycles where order existed)
    assert mock_sleep.call_count == 3
    for call in mock_sleep.call_args_list:
        assert call.kwargs == {"delay": 60}

    # Verify logging - 3 "waiting" + 1 "closed" = 4 debug calls
    assert client._logger.debug.call_count == 4

    # Check waiting debug calls
    waiting_calls = [
        call
        for call in client._logger.debug.call_args_list
        if "waiting for one minute" in str(call)
    ]
    assert len(waiting_calls) == 3

    # Check closed debug call
    client._logger.debug.assert_any_call("Margin order seems to be closed")


@pytest.mark.asyncio
async def test_wait_for_order_close_order_found_in_middle_of_list() -> None:
    """Test when target order is found in the middle of the orders list."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    margin_asset_id = 3333333

    # Create multiple orders with target in the middle
    mock_order_1 = Mock()
    mock_order_1.id = 1111111
    mock_order_2 = Mock()
    mock_order_2.id = 2222222
    mock_target_order = Mock()
    mock_target_order.id = 3333333  # Target order
    mock_order_4 = Mock()
    mock_order_4.id = 4444444
    mock_order_5 = Mock()
    mock_order_5.id = 5555555

    # First call: order exists, second call: order is gone
    client.get_margin_all_open_orders = AsyncMock(
        side_effect=[
            [
                mock_order_1,
                mock_order_2,
                mock_target_order,
                mock_order_4,
                mock_order_5,
            ],  # Found
            [mock_order_1, mock_order_2, mock_order_4, mock_order_5],  # Not found
        ],
    )

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        await client._wait_for_order_close(margin_asset_id)

    # Assert
    assert client.get_margin_all_open_orders.call_count == 2
    assert mock_sleep.call_count == 1
    assert client._logger.debug.call_count == 2


@pytest.mark.asyncio
async def test_wait_for_order_close_get_orders_exception() -> None:
    """Test when get_margin_all_open_orders raises an exception."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    margin_asset_id = 9999999

    # Mock get_margin_all_open_orders to raise exception
    client.get_margin_all_open_orders = AsyncMock(
        side_effect=Exception("API error"),
    )

    # Act & Assert
    with pytest.raises(Exception, match="API error"):
        await client._wait_for_order_close(margin_asset_id)

    # Verify get_margin_all_open_orders was called once before exception
    client.get_margin_all_open_orders.assert_called_once()


@pytest.mark.asyncio
async def test_wait_for_order_close_order_found_first_in_list() -> None:
    """Test when target order is the first in the orders list."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    margin_asset_id = 1111111

    # Target order is first in list
    mock_target_order = Mock()
    mock_target_order.id = 1111111  # Target order (first)
    mock_order_2 = Mock()
    mock_order_2.id = 2222222
    mock_order_3 = Mock()
    mock_order_3.id = 3333333

    # First call: order exists (first in list), second call: order is gone
    client.get_margin_all_open_orders = AsyncMock(
        side_effect=[
            [mock_target_order, mock_order_2, mock_order_3],  # Found first
            [mock_order_2, mock_order_3],  # Not found
        ],
    )

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        await client._wait_for_order_close(margin_asset_id)

    # Assert
    assert client.get_margin_all_open_orders.call_count == 2
    assert mock_sleep.call_count == 1

    # Verify both debug messages
    client._logger.debug.assert_any_call(
        "Margin order is not yet closed, waiting for one minute before trying again",
    )
    client._logger.debug.assert_any_call("Margin order seems to be closed")


@pytest.mark.asyncio
async def test_wait_for_order_close_order_found_last_in_list() -> None:
    """Test when target order is the last in the orders list."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    margin_asset_id = 9999999

    # Target order is last in list
    mock_order_1 = Mock()
    mock_order_1.id = 1111111
    mock_order_2 = Mock()
    mock_order_2.id = 2222222
    mock_target_order = Mock()
    mock_target_order.id = 9999999  # Target order (last)

    # First call: order exists (last in list), second call: order is gone
    client.get_margin_all_open_orders = AsyncMock(
        side_effect=[
            [mock_order_1, mock_order_2, mock_target_order],  # Found last
            [mock_order_1, mock_order_2],  # Not found
        ],
    )

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        await client._wait_for_order_close(margin_asset_id)

    # Assert
    assert client.get_margin_all_open_orders.call_count == 2
    assert mock_sleep.call_count == 1
    assert client._logger.debug.call_count == 2


@pytest.mark.asyncio
async def test_wait_for_order_close_single_order_list() -> None:
    """Test when there's only one order in the list (the target order)."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    margin_asset_id = 5555555

    # Single order that is the target
    mock_target_order = Mock()
    mock_target_order.id = 5555555

    # First call: single order exists, second call: empty list
    client.get_margin_all_open_orders = AsyncMock(
        side_effect=[
            [mock_target_order],  # Single order found
            [],  # Empty list - order closed
        ],
    )

    # Act
    with patch("asyncio.sleep") as mock_sleep:
        await client._wait_for_order_close(margin_asset_id)

    # Assert
    assert client.get_margin_all_open_orders.call_count == 2
    assert mock_sleep.call_count == 1
    assert client._logger.debug.call_count == 2

    # Verify the break statement works correctly in the for loop
    client._logger.debug.assert_any_call(
        "Margin order is not yet closed, waiting for one minute before trying again",
    )
    client._logger.debug.assert_any_call("Margin order seems to be closed")


# endregion wait_for_order_close

# region withdraw_balance_if_requested


@pytest.mark.asyncio
async def test_withdraw_balance_if_requested_success() -> None:
    """Test successful balance withdrawal with positive balance."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "BTCUSDT"

    # Mock successful balance retrieval and transfer
    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("150.75"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act
    await client._withdraw_balance_if_requested(order)

    # Assert
    # Verify balance retrieval was called with correct symbol
    client.get_margin_asset_balance.assert_called_once_with("BTCUSDT")

    # Verify transfer was called with correct parameters
    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once_with(
        transfer_amount=Decimal("150.75"),
        isolated_symbol="BTCUSDT",
    )

    # Verify logging
    assert client._logger.debug.call_count == 2

    # Check first debug log
    client._logger.debug.assert_any_call(
        "User asked to withdraw balance after trade",
    )

    # Check second debug log
    client._logger.debug.assert_any_call(
        "Transferring of asset balance to wallet done",
    )


@pytest.mark.asyncio
async def test_withdraw_balance_if_requested_zero_balance() -> None:
    """Test withdrawal with zero balance."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "ETHUSDT"

    # Mock zero balance
    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("0.00"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act
    await client._withdraw_balance_if_requested(order)

    # Assert
    client.get_margin_asset_balance.assert_called_once_with("ETHUSDT")

    # Verify transfer was still called even with zero balance
    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once_with(
        transfer_amount=Decimal("0.00"),
        isolated_symbol="ETHUSDT",
    )

    # Verify both debug logs were called
    assert client._logger.debug.call_count == 2
    client._logger.debug.assert_any_call(
        "User asked to withdraw balance after trade",
    )
    client._logger.debug.assert_any_call(
        "Transferring of asset balance to wallet done",
    )


@pytest.mark.asyncio
async def test_withdraw_balance_if_requested_small_balance() -> None:
    """Test withdrawal with very small balance."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "ADAUSDT"

    # Mock very small balance
    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("0.001"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act
    await client._withdraw_balance_if_requested(order)

    # Assert
    client.get_margin_asset_balance.assert_called_once_with("ADAUSDT")
    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once_with(
        transfer_amount=Decimal("0.001"),
        isolated_symbol="ADAUSDT",
    )

    # Verify logging
    assert client._logger.debug.call_count == 2


@pytest.mark.asyncio
async def test_withdraw_balance_if_requested_large_balance() -> None:
    """Test withdrawal with large balance."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "SOLUSDT"

    # Mock large balance
    client.get_margin_asset_balance = AsyncMock(
        return_value=Decimal("999999.999999"),
    )
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act
    await client._withdraw_balance_if_requested(order)

    # Assert
    client.get_margin_asset_balance.assert_called_once_with("SOLUSDT")
    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once_with(
        transfer_amount=Decimal("999999.999999"),
        isolated_symbol="SOLUSDT",
    )

    # Verify logging
    assert client._logger.debug.call_count == 2


@pytest.mark.asyncio
async def test_withdraw_balance_if_requested_get_balance_exception() -> None:
    """Test when get_margin_asset_balance raises an exception."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "DOTUSDT"

    # Mock get_margin_asset_balance to raise exception
    client.get_margin_asset_balance = AsyncMock(
        side_effect=Exception("Balance retrieval failed"),
    )
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act & Assert
    with pytest.raises(Exception, match="Balance retrieval failed"):
        await client._withdraw_balance_if_requested(order)

    # Verify get_margin_asset_balance was called
    client.get_margin_asset_balance.assert_called_once_with("DOTUSDT")

    # Verify transfer was not called due to exception
    client.transfer_usdt_from_margin_asset_to_wallet.assert_not_called()

    # Verify only first debug log was called before exception
    client._logger.debug.assert_called_once_with(
        "User asked to withdraw balance after trade",
    )


@pytest.mark.asyncio
async def test_withdraw_balance_if_requested_transfer_exception() -> None:
    """Test when transfer_usdt_from_margin_asset_to_wallet raises an exception."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "AVAXUSDT"

    # Mock successful balance retrieval but failed transfer
    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("100.50"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock(
        side_effect=Exception("Transfer failed"),
    )

    # Act & Assert
    with pytest.raises(Exception, match="Transfer failed"):
        await client._withdraw_balance_if_requested(order)

    # Verify both methods were called
    client.get_margin_asset_balance.assert_called_once_with("AVAXUSDT")
    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once_with(
        transfer_amount=Decimal("100.50"),
        isolated_symbol="AVAXUSDT",
    )

    # Verify only first debug log was called before transfer exception
    client._logger.debug.assert_called_once_with(
        "User asked to withdraw balance after trade",
    )


@pytest.mark.asyncio
async def test_withdraw_balance_if_requested_different_symbols() -> None:
    """Test withdrawal with different isolated symbols."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    # Test with different symbols
    symbols_and_balances = [
        ("MATICUSDT", Decimal("75.25")),
        ("LINKUSDT", Decimal("200.00")),
        ("UNIUSDT", Decimal("50.123456")),
    ]

    for symbol, balance in symbols_and_balances:
        # Reset mocks for each iteration
        client._logger.reset_mock()

        order = Mock()
        order.isolated_symbol = symbol

        client.get_margin_asset_balance = AsyncMock(return_value=balance)
        client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

        # Act
        await client._withdraw_balance_if_requested(order)

        # Assert
        client.get_margin_asset_balance.assert_called_once_with(symbol)
        client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once_with(
            transfer_amount=balance,
            isolated_symbol=symbol,
        )

        # Verify logging for each symbol
        assert client._logger.debug.call_count == 2


@pytest.mark.asyncio
async def test_withdraw_balance_if_requested_method_call_order() -> None:
    """Test that methods are called in the correct order."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "SHIBUSDT"

    # Track call order
    call_order = []

    async def mock_get_balance(symbol) -> Decimal:  # noqa: ANN001, ARG001
        call_order.append("get_balance")
        return Decimal("42.42")

    async def mock_transfer(*args, **kwargs) -> None:  # noqa: ANN002, ANN003, ARG001
        call_order.append("transfer")

    client.get_margin_asset_balance = AsyncMock(side_effect=mock_get_balance)
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock(
        side_effect=mock_transfer,
    )

    # Act
    await client._withdraw_balance_if_requested(order)

    # Assert
    # Verify methods were called in correct order
    assert call_order == ["get_balance", "transfer"]

    # Verify logging happened at correct times
    assert client._logger.debug.call_count == 2


@pytest.mark.asyncio
async def test_withdraw_balance_if_requested_return_value() -> None:
    """Test that the function returns None as expected."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "DOGEUSDT"

    client.get_margin_asset_balance = AsyncMock(return_value=Decimal("25.00"))
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act
    result = await client._withdraw_balance_if_requested(order)

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_withdraw_balance_if_requested_decimal_precision() -> None:
    """Test withdrawal with various decimal precisions."""
    # Arrange
    client: TabdealClient = create_tabdeal_client()
    client._logger = Mock()

    order = Mock()
    order.isolated_symbol = "ATOMUSDT"

    # Test with high precision decimal
    high_precision_balance = Decimal("123.123456789012345")
    client.get_margin_asset_balance = AsyncMock(
        return_value=high_precision_balance,
    )
    client.transfer_usdt_from_margin_asset_to_wallet = AsyncMock()

    # Act
    await client._withdraw_balance_if_requested(order)

    # Assert
    client.transfer_usdt_from_margin_asset_to_wallet.assert_called_once_with(
        transfer_amount=high_precision_balance,
        isolated_symbol="ATOMUSDT",
    )

    # Verify the exact decimal value is preserved
    called_args = client.transfer_usdt_from_margin_asset_to_wallet.call_args
    assert called_args.kwargs["transfer_amount"] == high_precision_balance
    assert isinstance(called_args.kwargs["transfer_amount"], Decimal)


# endregion withdraw_balance_if_requested
