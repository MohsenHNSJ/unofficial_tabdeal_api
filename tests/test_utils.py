"""This module is for testing the functions of utils module."""
# ruff: noqa: S101

from decimal import Decimal
from typing import Any

import pytest

from tests.test_constants import (
    EXPECTED_SESSION_HEADERS,
    SAMPLE_DECIMAL_FLOAT_LOW,
    SAMPLE_DECIMAL_FLOAT_VERY_LOW,
    SAMPLE_DECIMAL_INT_HIGH,
    SAMPLE_DECIMAL_INT_VERY_HIGH,
    SAMPLE_DECIMAL_STR_HIGH,
    SAMPLE_DECIMAL_STR_LOW,
    SAMPLE_DECIMAL_STR_VERY_HIGH,
    SAMPLE_DECIMAL_STR_VERY_LOW,
    SAMPLE_JSON_DATA,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from unofficial_tabdeal_api.utils import (
    create_session_headers,
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
    # pragma: no cover
    if isinstance(processed_data, dict):
        assert ((processed_data["markets"])[0])["market_id"] == 1
    # pragma: no cover
    else:
        pytest.fail("Data is processed to wrong type!")
