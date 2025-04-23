"""This module holds the utility functions needed by the TabdealClient class."""

# mypy: disable-error-code="type-arg,assignment"

from decimal import Decimal


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
