"""This module holds the enums."""

from enum import Enum


class DryRun(Enum):
    """Enum class to indicate wether to dry run or not."""

    YES = 1
    """Run as a Dry-run"""
    NO = 2
    """Don't run as a Dry-run"""
