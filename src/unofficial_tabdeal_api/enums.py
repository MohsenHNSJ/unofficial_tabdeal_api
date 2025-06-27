"""This module holds the enums."""

from enum import Enum


class DryRun(Enum):
    """Enum class to indicate whether to dry run or not."""

    YES = 1
    """Run as a Dry-run"""
    NO = 2
    """Don't run as a Dry-run"""


class OrderState(Enum):
    """Enum class to indicate the state of order."""

    PENDING = 1
    UNKNOWN_TWO = 2  # Not yet encountered
    UNKNOWN_THREE = 3  # Not yet encountered
    FILLED = 4
    CANCELED = 5


class OrderSide(Enum):
    """Enum class to indicate the side of order."""

    BUY = 1
    """Buy order"""
    SELL = 2
    """Sell order"""


class MathOperation(Enum):
    """Enum class to indicate the math operation."""

    ADD = 1
    """Addition"""
    SUBTRACT = 2
    """Subtraction"""
    MULTIPLY = 3
    """Multiplication"""
    DIVIDE = 4
    """Division"""
