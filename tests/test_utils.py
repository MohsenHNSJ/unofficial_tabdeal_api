"""This module is for testing the functions of utils module."""
# ruff: noqa: S101, PLR0913
# pylint: disable=R0913

from decimal import Decimal
from typing import Any

import pytest

from unofficial_tabdeal_api.enums import MathOperation, OrderSide
from unofficial_tabdeal_api.utils import (
    calculate_order_volume,
    calculate_sl_tp_prices,
    calculate_usdt,
    isolated_symbol_to_tabdeal_symbol,
    normalize_decimal,
    process_server_response,
)

# region TEST_DATA
normalize_decimal_test_data: list[tuple[str | float, str | float]] = [
    (
        2592500000000000000000000000000000000000000000000000,
        2592500000000000000000000000000000000000000000000000,
    ),
    ("2.5925E+51", 2592500000000000000000000000000000000000000000000000),
    (375000000000000000000000, 375000000000000000000000),
    ("375000000000000000000000", 375000000000000000000000),
    ("0.0000000000002", "2E-13"),
    ("2E-13", "2E-13"),
    ("0.00000000000000000000000000000000000000043235", "4.3235E-40"),
    ("4.3235E-40", "4.3235E-40"),
    (0, 0),
    (1, 1),
]

process_server_response_test_data: list[tuple[str, dict[str, Any] | list[dict[str, Any]]]] = [
    (
        '{"markets":[{"spot_grid_bot_active":false,"market_id":1},{"market_id":2}]}',
        {
            "markets": [
                {
                    "spot_grid_bot_active": False,
                    "market_id": 1,
                },
                {"market_id": 2},
            ],
        },
    ),
    (
        '{"markets":[{"spot_grid_bot_active":true,"market_id":3},{"market_id":4}]}',
        {
            "markets": [
                {
                    "spot_grid_bot_active": True,
                    "market_id": 3,
                },
                {"market_id": 4},
            ],
        },
    ),
    (
        '{"markets":[{"spot_grid_bot_active":false,"market_id":5}]}',
        {"markets": [{"spot_grid_bot_active": False, "market_id": 5}]},
    ),
]

calculate_order_volume_test_data: list[tuple[Decimal, Decimal, bool, Decimal, int]] = [
    (Decimal("2491.267"), Decimal("42.197"), False, Decimal(59), 0),
    (Decimal("45798.98347"), Decimal("367.684"), True, Decimal("124.560719"), 6),
]

calculate_usdt_test_data: list[tuple[Decimal, Decimal, MathOperation, Decimal]] = [
    (
        Decimal("17.3612348796"),
        Decimal("2.946625787"),
        MathOperation.ADD,
        Decimal("20.30786066"),
    ),
    (
        Decimal("26.3612348796756"),
        Decimal("19.715946625787"),
        MathOperation.SUBTRACT,
        Decimal("6.64528825"),
    ),
    (
        Decimal("860.0000000000001"),
        Decimal("20.0000000000002"),
        MathOperation.MULTIPLY,
        Decimal("17200.00000000"),
    ),
    (
        Decimal("105370.9244441"),
        Decimal("83.74528"),
        MathOperation.DIVIDE,
        Decimal("1258.23120352"),
    ),
]

isolated_symbol_to_tabdeal_symbol_test_data: list[tuple[str, str]] = [
    ("BTCUSDT", "BTC_USDT"),
    ("IUSDT", "I_USDT"),
    ("DAUYIASOUSDT", "DAUYIASO_USDT"),
]

calculate_sl_tp_prices_test_data: list[
    tuple[
        Decimal,
        OrderSide,
        Decimal,
        Decimal,
        Decimal,
        int,
        bool,
        tuple[Decimal, Decimal],
    ]
] = [
    (
        Decimal(1),
        OrderSide.BUY,
        Decimal(100),
        Decimal(5),
        Decimal(10),
        4,
        True,
        (Decimal(95), Decimal(110)),
    ),
    (
        Decimal(5),
        OrderSide.SELL,
        Decimal(200),
        Decimal(
            10,
        ),
        Decimal(20),
        0,
        False,
        (Decimal(204), Decimal(192)),
    ),
]
# endregion TEST_DATA


@pytest.mark.benchmark
@pytest.mark.parametrize(
    argnames=("input_value", "expected_value"),
    argvalues=normalize_decimal_test_data,
)
async def test_normalize_decimal(input_value: str | float, expected_value: str | float) -> None:
    """Tests the normalize_decimal function."""
    # Check values with expected results
    assert str(normalize_decimal(input_decimal=Decimal(input_value))) == str(
        expected_value,
    )

    # Python will often optimize the internal representation and reintroduce the exponent notation
    # (e.g., 2E-13) because that's how Decimal is designed: to represent numbers precisely,
    # not necessarily to preserve formatting preferences like fixed-point.
    # So, here's the key insight:
    # Decimal will internally store small numbers with exponent form if it's shorter and equivalent.
    # There's no way to "force" Decimal to never use exponent form internally.
    # It will always use the most efficient representation.

    # However, you can control how you display or format the Decimal value.
    # When you need to output it in fixed-point format (as a string)


@pytest.mark.benchmark
@pytest.mark.parametrize(
    argnames=("input_json", "processed_data"),
    argvalues=process_server_response_test_data,
)
async def test_process_server_response(
    *,
    input_json: str,
    processed_data: dict[
        str,
        Any,
    ]
    | list[dict[str, Any]],
) -> None:
    """Tests the process_server_response function."""
    # First we process the sample json data
    assert (
        await process_server_response(
            response=input_json,
        )
        == processed_data
    )


@pytest.mark.benchmark
@pytest.mark.parametrize(
    argnames=(
        "asset_balance",
        "order_price",
        "volume_fraction_allowed",
        "result",
        "required_precision",
    ),
    argvalues=calculate_order_volume_test_data,
)
async def test_calculate_order_volume(
    *,
    asset_balance: Decimal,
    order_price: Decimal,
    volume_fraction_allowed: bool,
    result: Decimal,
    required_precision: int,
) -> None:
    """Tests the calculate_order_volume function."""
    # Check sample values
    assert (
        calculate_order_volume(
            asset_balance=asset_balance,
            order_price=order_price,
            volume_fraction_allowed=volume_fraction_allowed,
            required_precision=required_precision,
        )
        == result
    )


@pytest.mark.benchmark
@pytest.mark.parametrize(
    argnames=("variable_one", "variable_two", "operation", "result"),
    argvalues=calculate_usdt_test_data,
)
async def test_calculate_usdt(
    *,
    variable_one: Decimal,
    variable_two: Decimal,
    operation: MathOperation,
    result: Decimal,
) -> None:
    """Tests the calculate_usdt function."""
    # Check sample operations
    assert (
        calculate_usdt(
            variable_one=variable_one,
            variable_two=variable_two,
            operation=operation,
        )
        == result
    )


@pytest.mark.benchmark
@pytest.mark.parametrize(
    argnames=("isolated_symbol", "expected_tabdeal_symbol"),
    argvalues=isolated_symbol_to_tabdeal_symbol_test_data,
)
async def test_isolated_symbol_to_tabdeal_symbol(
    *,
    isolated_symbol: str,
    expected_tabdeal_symbol: str,
) -> None:
    """Tests the isolated_symbol_to_tabdeal_symbol function."""
    # Check sample isolated symbol
    assert (
        isolated_symbol_to_tabdeal_symbol(isolated_symbol=isolated_symbol)
        == expected_tabdeal_symbol
    )


@pytest.mark.benchmark
@pytest.mark.parametrize(
    argnames=(
        "margin_level",
        "order_side",
        "break_even_point",
        "stop_loss_percent",
        "take_profit_percent",
        "price_required_precision",
        "price_fraction_allowed",
        "expected_result",
    ),
    argvalues=calculate_sl_tp_prices_test_data,
)
async def test_calculate_sl_tp_prices(
    *,
    margin_level: Decimal,
    order_side: OrderSide,
    break_even_point: Decimal,
    stop_loss_percent: Decimal,
    take_profit_percent: Decimal,
    price_required_precision: int,
    price_fraction_allowed: bool,
    expected_result: tuple[Decimal, Decimal],
) -> None:
    """Tests the calculate_sl_tp_prices function."""
    # Check test data
    assert expected_result == await calculate_sl_tp_prices(
        margin_level=margin_level,
        order_side=order_side,
        break_even_point=break_even_point,
        stop_loss_percent=stop_loss_percent,
        take_profit_percent=take_profit_percent,
        price_required_precision=price_required_precision,
        price_fraction_allowed=price_fraction_allowed,
    )
