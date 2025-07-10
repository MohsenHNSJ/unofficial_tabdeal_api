"""This module holds the utility functions needed by the TabdealClient class."""

# mypy: disable-error-code="type-arg,assignment"

import json
from decimal import ROUND_DOWN, Decimal, getcontext, setcontext
from typing import TYPE_CHECKING, Any

from aiohttp import ClientResponse

from unofficial_tabdeal_api.constants import DECIMAL_PRECISION, REQUIRED_USDT_PRECISION
from unofficial_tabdeal_api.enums import MathOperation, OrderSide

if TYPE_CHECKING:  # pragma: no cover
    from decimal import Context


def normalize_decimal(input_decimal: Decimal) -> Decimal:
    """Normalizes the fractions of a decimal value.

    Removes excess trailing zeros and exponents

    Args:
        input_decimal (Decimal): Input decimal

    Returns:
        Decimal: Normalized decimal
    """
    # First we set the decimal context settings
    # Get the decimal context
    decimal_context: Context = getcontext()

    # Set Precision
    decimal_context.prec = DECIMAL_PRECISION

    # Set rounding method
    decimal_context.rounding = ROUND_DOWN

    # Set decimal context
    setcontext(decimal_context)

    # First we normalize the decimal using built-in normalizer
    normalized_decimal: Decimal = input_decimal.normalize()

    # Then we extract sign, digits and exponents from the decimal value
    exponent: int  # Number of exponents
    sign: int  # Stores [0] for positive values and [1] for negative values
    digits: tuple  # A tuple of digits until reaching an exponent # type: ignore[]

    sign, digits, exponent = normalized_decimal.as_tuple()  # type: ignore[]

    # If decimal has exponent, remove it
    if exponent > 0:
        return Decimal((sign, digits + (0,) * exponent, 0))

    # Else, return the normalized decimal
    return normalized_decimal


async def process_server_response(
    response: ClientResponse | str,
) -> dict[str, Any] | list[dict[str, Any]]:
    """Processes the raw response from server and converts it into python objects.

    Args:
        response (ClientResponse | str): Response from server or a string

    Returns:
        dict[str, Any] | list[dict[str, Any]]: a Dictionary or a list of dictionaries
    """
    # First, if we received ClientResponse, we extract response content as string from it
    json_string: str
    # If it's plain string, we use it as is
    if isinstance(response, str):
        json_string = response
    else:
        json_string = await response.text()

    # Then we convert the response to python object
    response_data: dict[str, Any] | list[dict[str, Any]] = json.loads(json_string)

    # And finally we return it
    return response_data


def calculate_order_volume(
    *,
    asset_balance: Decimal,
    order_price: Decimal,
    volume_fraction_allowed: bool,
    required_precision: int = 0,
    order_side: OrderSide,
) -> Decimal:
    """Calculates the order volume based on the asset balance and order price.

    Args:
        asset_balance (Decimal): Balance available in asset
        order_price (Decimal): Price of the order
        volume_fraction_allowed (bool): If volume fraction is allowed
        required_precision (int): Required precision for the order volume. Defaults to 0.
        order_side (OrderSide): Side of the order (BUY or SELL)

    Returns:
        Decimal: Calculated order volume
    """
    # First we set the decimal context settings
    # Get the decimal context
    decimal_context: Context = getcontext()

    # Set Precision
    decimal_context.prec = DECIMAL_PRECISION

    # Set rounding method
    decimal_context.rounding = ROUND_DOWN

    # Set decimal context
    setcontext(decimal_context)

    # Calculate order volume
    order_volume: Decimal = decimal_context.divide(
        asset_balance,
        order_price,
    )

    # When the order is SELL, Tabdeal doesn't allow all of the borrow-able amount to be used,
    # This is actually usable when the order is BUY, but on SELL, for unknown reasons, it isn't.
    # Based on my observations, Tabdeal holds 0.68% to 0.77% of the borrow-able amount,
    # so we have to reduce the order volume by an amount to make sure it's acceptable.
    # I chose to reduce the order volume by 1% to be on the safe side.
    if order_side is OrderSide.SELL:
        # Reduce the order volume by 1%
        order_volume = decimal_context.multiply(order_volume, Decimal("0.99"))

    # If volume fraction is not allowed, we round it down
    if not volume_fraction_allowed:
        order_volume = order_volume.to_integral_value()
    # Else, we quantize it to required precision
    else:
        order_volume = order_volume.quantize(
            Decimal("1." + "0" * required_precision),
            rounding=ROUND_DOWN,
        )

    return order_volume


def calculate_usdt(
    *,
    variable_one: Decimal,
    variable_two: Decimal,
    operation: MathOperation,
) -> Decimal:
    """Calculates the USDT value based on the operation.

    Args:
        variable_one (Decimal): First variable
        variable_two (Decimal): Second variable
        operation (MathOperation): Math operation to perform

    Returns:
        Decimal: Calculated USDT value
    """
    # First we set the decimal context settings
    # Get the decimal context
    decimal_context: Context = getcontext()

    # Set Precision
    decimal_context.prec = DECIMAL_PRECISION

    # Set rounding method
    decimal_context.rounding = ROUND_DOWN

    # Set decimal context
    setcontext(decimal_context)

    usdt_value: Decimal

    # Calculate USDT value based on the operation
    if operation == MathOperation.ADD:
        usdt_value = decimal_context.add(variable_one, variable_two)
    elif operation == MathOperation.SUBTRACT:
        usdt_value = decimal_context.subtract(variable_one, variable_two)
    elif operation == MathOperation.MULTIPLY:
        usdt_value = decimal_context.multiply(variable_one, variable_two)
    else:
        usdt_value = decimal_context.divide(
            variable_one,
            variable_two,
        )

    # Quantize to required precision
    usdt_value = usdt_value.quantize(
        Decimal("1." + "0" * REQUIRED_USDT_PRECISION),
        rounding=ROUND_DOWN,
    )

    return usdt_value


def isolated_symbol_to_tabdeal_symbol(isolated_symbol: str) -> str:
    """Converts the isolated symbol to Tabdeal symbol.

    Args:
        isolated_symbol (str): Isolated symbol

    Returns:
        str: Tabdeal symbol
    """
    # Replace USDT with _USDT
    tabdeal_symbol: str = isolated_symbol.replace("USDT", "_USDT")

    return tabdeal_symbol


def calculate_sl_tp_prices(  # noqa: PLR0913
    *,
    margin_level: Decimal,
    order_side: OrderSide,
    break_even_point: Decimal,
    stop_loss_percent: Decimal,
    take_profit_percent: Decimal,
    price_required_precision: int,
    price_fraction_allowed: bool,
) -> tuple[Decimal, Decimal]:
    """Calculates the Stop Loss and Take Profit price points.

    Args:
        margin_level (Decimal): Margin level of the order
        order_side (OrderSide): Side of the order
        break_even_point (Decimal): Price that yields no loss and no profit
        stop_loss_percent (Decimal): Percent of tolerate-able loss
        take_profit_percent (Decimal): Expected percent of profit
        price_required_precision (int): Required amount of precision for price by server
        price_fraction_allowed (bool): Is fractions allowed for price?

    Returns:
        tuple[Decimal, Decimal]: a Tuple containing Stop Loss and Take Profit
    """
    # First we set the decimal context settings
    # Get the decimal context
    decimal_context: Context = getcontext()

    # Set Precision
    decimal_context.prec = DECIMAL_PRECISION

    # Set rounding method
    decimal_context.rounding = ROUND_DOWN

    # Set decimal context
    setcontext(decimal_context)

    # Then we calculate the percent of difference required for each according to margin level
    sl_percent_diff: Decimal = decimal_context.divide(
        stop_loss_percent,
        margin_level,
    )
    tp_percent_diff: Decimal = decimal_context.divide(
        take_profit_percent,
        margin_level,
    )

    # Then we calculate the percentile
    # Here, side of the order matters
    sl_percentile: Decimal
    tp_percentile: Decimal
    if order_side is OrderSide.BUY:
        sl_percentile = decimal_context.subtract(
            Decimal(100),
            sl_percent_diff,
        )
        tp_percentile = decimal_context.add(
            Decimal(100),
            tp_percent_diff,
        )
    else:  # Else must be a SELL side (Short order)
        sl_percentile = decimal_context.add(
            Decimal(100),
            sl_percent_diff,
        )
        tp_percentile = decimal_context.subtract(
            Decimal(100),
            tp_percent_diff,
        )

    # Finally we calculate the prices
    sl_price: Decimal = decimal_context.divide(
        decimal_context.multiply(
            sl_percentile,
            break_even_point,
        ),
        Decimal(100),
    )
    tp_price: Decimal = decimal_context.divide(
        decimal_context.multiply(
            tp_percentile,
            break_even_point,
        ),
        Decimal(100),
    )

    # If price fraction is not allowed, we round it down
    if not price_fraction_allowed:
        sl_price = sl_price.to_integral_value()
        tp_price = tp_price.to_integral_value()
    # Else, we quantize it to required precision
    else:
        sl_price = sl_price.quantize(
            Decimal("1." + "0" * price_required_precision),
            rounding=ROUND_DOWN,
        )
        tp_price = tp_price.quantize(
            Decimal("1." + "0" * price_required_precision),
            rounding=ROUND_DOWN,
        )

    # And return the variables
    return sl_price, tp_price


def find_order_by_id(
    *,
    orders_list: list[dict[str, Any]],
    order_id: str | int,
) -> dict[str, Any] | None:
    """Finds an order by its ID in the list of orders.

    Args:
        orders_list (list[dict[str, Any]]): List of orders
        order_id (str | int): ID of the order to find

    Returns:
        dict[str, Any] | None: The found order or None if not found
    """
    for order in orders_list:
        if order.get("id") == order_id:
            return order
    return None
