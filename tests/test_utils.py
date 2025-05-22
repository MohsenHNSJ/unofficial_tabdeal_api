"""This module is for testing the functions of utils module."""
# ruff: noqa: S101

from decimal import Decimal
from typing import Any

import pytest

from tests.test_constants import (
    EXPECTED_SESSION_HEADERS,
    FIRST_SAMPLE_ASSET_BALANCE,
    FIRST_SAMPLE_ORDER_PRICE,
    SAMPLE_DECIMAL_FLOAT_LOW,
    SAMPLE_DECIMAL_FLOAT_VERY_LOW,
    SAMPLE_DECIMAL_INT_HIGH,
    SAMPLE_DECIMAL_INT_VERY_HIGH,
    SAMPLE_DECIMAL_STR_HIGH,
    SAMPLE_DECIMAL_STR_LOW,
    SAMPLE_DECIMAL_STR_VERY_HIGH,
    SAMPLE_DECIMAL_STR_VERY_LOW,
    SAMPLE_JSON_DATA,
    SECOND_SAMPLE_ASSET_BALANCE,
    SECOND_SAMPLE_ORDER_PRICE,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from unofficial_tabdeal_api.enums import MathOperation
from unofficial_tabdeal_api.utils import (
    calculate_order_volume,
    calculate_usdt,
    create_session_headers,
    isolated_symbol_to_tabdeal_symbol,
    normalize_decimal,
    process_server_response,
)


@pytest.mark.benchmark
def test_create_session_headers() -> None:
    """Tests the function of create_session_headers."""
    # Create session headers using test data
    result = create_session_headers(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
    )
    # Check if received data is as expected
    assert result == EXPECTED_SESSION_HEADERS


@pytest.mark.benchmark
async def test_normalize_decimal() -> None:
    """Tests the normalize_decimal function."""
    # Check very high value as integer
    assert str(await normalize_decimal(Decimal(SAMPLE_DECIMAL_INT_VERY_HIGH))) == str(
        SAMPLE_DECIMAL_INT_VERY_HIGH,
    )
    # Check very high value as string
    assert str(await normalize_decimal(Decimal(SAMPLE_DECIMAL_STR_VERY_HIGH))) == str(
        SAMPLE_DECIMAL_INT_VERY_HIGH,
    )
    # Check high value as integer
    assert str(await normalize_decimal(Decimal(SAMPLE_DECIMAL_INT_HIGH))) == str(
        SAMPLE_DECIMAL_INT_HIGH,
    )
    # Check high value as string
    assert str(await normalize_decimal(Decimal(SAMPLE_DECIMAL_STR_HIGH))) == str(
        SAMPLE_DECIMAL_INT_HIGH,
    )
    # Python will often optimize the internal representation and reintroduce the exponent notation
    # (e.g., 2E-13) because that's how Decimal is designed: to represent numbers precisely,
    # not necessarily to preserve formatting preferences like fixed-point.
    # So, here's the key insight:
    # Decimal will internally store small numbers with exponent form if it's shorter and equivalent.
    # There's no way to "force" Decimal to never use exponent form internally.
    # # When you need to output it in fixed-point format (as a string)
    # fixed_str = format(num, 'f')
    # Check low value as float
    assert str(await normalize_decimal(Decimal(SAMPLE_DECIMAL_FLOAT_LOW))) == SAMPLE_DECIMAL_STR_LOW
    assert format((await normalize_decimal(Decimal(SAMPLE_DECIMAL_FLOAT_LOW))), "f") == str(
        SAMPLE_DECIMAL_FLOAT_LOW,
    )
    # Check low value as string
    assert str(await normalize_decimal(Decimal(SAMPLE_DECIMAL_STR_LOW))) == SAMPLE_DECIMAL_STR_LOW
    assert format((await normalize_decimal(Decimal(SAMPLE_DECIMAL_STR_LOW))), "f") == str(
        SAMPLE_DECIMAL_FLOAT_LOW,
    )
    # Check very low value as float
    assert (
        str(await normalize_decimal(Decimal(SAMPLE_DECIMAL_FLOAT_VERY_LOW)))
        == SAMPLE_DECIMAL_STR_VERY_LOW
    )
    assert format((await normalize_decimal(Decimal(SAMPLE_DECIMAL_FLOAT_VERY_LOW))), "f") == str(
        SAMPLE_DECIMAL_FLOAT_VERY_LOW,
    )
    # Check very low value as string
    assert (
        str(await normalize_decimal(Decimal(SAMPLE_DECIMAL_STR_VERY_LOW)))
        == SAMPLE_DECIMAL_STR_VERY_LOW
    )
    assert format((await normalize_decimal(Decimal(SAMPLE_DECIMAL_STR_VERY_LOW))), "f") == str(
        SAMPLE_DECIMAL_FLOAT_VERY_LOW,
    )
    # Check value 0
    assert str(await normalize_decimal(Decimal(0))) == str(0)
    # Check value 1
    assert str(await normalize_decimal(Decimal(1))) == str(1)


@pytest.mark.benchmark
async def test_process_server_response() -> None:
    """Tests the process_server_response function."""
    # First we process the sample json data
    processed_data: dict[str, Any] | list[dict[str, Any]] = await process_server_response(
        SAMPLE_JSON_DATA,
    )

    # Last, we will assert it's validity
    if isinstance(processed_data, dict):  # pragma: no cover
        assert ((processed_data["markets"])[0])["market_id"] == 1
    else:
        pytest.fail("Data is processed to wrong type!")  # pragma: no cover


@pytest.mark.benchmark
async def test_calculate_order_volume() -> None:
    """Tests the calculate_order_volume function."""
    # Check first sample value
    first_sample_result: Decimal = await calculate_order_volume(
        asset_balance=FIRST_SAMPLE_ASSET_BALANCE,
        order_price=FIRST_SAMPLE_ORDER_PRICE,
        volume_fraction_allowed=False,
    )
    assert first_sample_result == Decimal("59")

    # Check second sample value
    # Generate custom context for the second sample
    # to allow up to 6 decimal places
    second_sample_result: Decimal = await calculate_order_volume(
        asset_balance=SECOND_SAMPLE_ASSET_BALANCE,
        order_price=SECOND_SAMPLE_ORDER_PRICE,
        volume_fraction_allowed=True,
        required_precision=6,
    )
    assert second_sample_result == Decimal("124.560719")


@pytest.mark.benchmark
async def test_calculate_usdt() -> None:
    """Tests the calculate_usdt function."""
    # Check sample addition
    sample_addition: Decimal = await calculate_usdt(
        variable_one=Decimal("17.3612348796"),
        variable_two=Decimal("2.946625787"),
        operation=MathOperation.ADD,
    )
    assert sample_addition == Decimal("20.30786066")

    # Check sample subtraction
    sample_subtraction: Decimal = await calculate_usdt(
        variable_one=Decimal("26.3612348796756"),
        variable_two=Decimal("19.715946625787"),
        operation=MathOperation.SUBTRACT,
    )
    assert sample_subtraction == Decimal("6.64528825")

    # Check sample multiplication
    sample_multiplication: Decimal = await calculate_usdt(
        variable_one=Decimal("860.0000000000001"),
        variable_two=Decimal("20.0000000000002"),
        operation=MathOperation.MULTIPLY,
    )
    assert sample_multiplication == Decimal("17200.00000000")

    # Check sample division
    sample_division: Decimal = await calculate_usdt(
        variable_one=Decimal("105370.9244441"),
        variable_two=Decimal("83.74528"),
        operation=MathOperation.DIVIDE,
    )
    assert sample_division == Decimal("1258.23120352")


@pytest.mark.benchmark
async def test_isolated_symbol_to_tabdeal_symbol() -> None:
    """Tests the isolated_symbol_to_tabdeal_symbol function."""
    # Check sample isolated symbol
    first_sample_isolated_symbol: str = "BTCUSDT"
    first_expected_tabdeal_symbol: str = "BTC_USDT"
    assert (
        await isolated_symbol_to_tabdeal_symbol(first_sample_isolated_symbol)
        == first_expected_tabdeal_symbol
    )

    # Check sample isolated symbol
    second_sample_isolated_symbol: str = "DAUYIASOUSDT"
    second_expected_tabdeal_symbol: str = "DAUYIASO_USDT"
    assert (
        await isolated_symbol_to_tabdeal_symbol(second_sample_isolated_symbol)
        == second_expected_tabdeal_symbol
    )

    # Check sample isolated symbol
    third_sample_isolated_symbol: str = "IUSDT"
    third_expected_tabdeal_symbol: str = "I_USDT"
    assert (
        await isolated_symbol_to_tabdeal_symbol(third_sample_isolated_symbol)
        == third_expected_tabdeal_symbol
    )
