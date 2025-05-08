"""This module holds the utility functions needed by the TabdealClient class."""

# mypy: disable-error-code="type-arg,assignment"

import json
from decimal import ROUND_DOWN, Decimal, getcontext, setcontext
from typing import TYPE_CHECKING, Any

from aiohttp import ClientResponse

from unofficial_tabdeal_api.constants import DECIMAL_PRECISION

if TYPE_CHECKING:
    from decimal import Context


def create_session_headers(user_hash: str, authorization_key: str) -> dict[str, str]:
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
