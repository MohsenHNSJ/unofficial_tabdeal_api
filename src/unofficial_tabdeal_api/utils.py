"""This module holds the utility functions needed by the TabdealClient class."""

# mypy: disable-error-code="type-arg,assignment"

import json
from decimal import ROUND_DOWN, Decimal, getcontext, setcontext
from typing import TYPE_CHECKING, Any

from aiohttp import ClientResponse

from unofficial_tabdeal_api.constants import DECIMAL_PRECISION, REQUIRED_USDT_PRECISION
from unofficial_tabdeal_api.enums import MathOperation

if TYPE_CHECKING:  # pragma: no cover
    from decimal import Context


def create_session_headers(*, user_hash: str, authorization_key: str) -> dict[str, str]:
    """Creates the header fo aiohttp client session.

    Args:
        user_hash (str): User hash
        authorization_key (str): User authorization key

    Returns:
        dict[str, str]: Client session header
    """
    session_headers: dict[str, str] = {
        "user-hash": user_hash,
        "Authorization": authorization_key,
    }

    return session_headers


async def normalize_decimal(input_decimal: Decimal) -> Decimal:
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


async def calculate_order_volume(
    *,
    asset_balance: Decimal,
    order_price: Decimal,
    volume_fraction_allowed: bool,
    required_precision: int = 0,
) -> Decimal:
    """Calculates the order volume based on the asset balance and order price.

    Args:
        asset_balance (Decimal): Balance available in asset
        order_price (Decimal): Price of the order
        volume_fraction_allowed (bool): If volume fraction is allowed
        required_precision (int): Required precision for the order volume. Defaults to 0.

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


async def calculate_usdt(
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


async def isolated_symbol_to_tabdeal_symbol(isolated_symbol: str) -> str:
    """Converts the isolated symbol to Tabdeal symbol.

    Args:
        isolated_symbol (str): Isolated symbol

    Returns:
        str: Tabdeal symbol
    """
    # Replace USDT with _USDT
    tabdeal_symbol: str = isolated_symbol.replace("USDT", "_USDT")

    return tabdeal_symbol
