"""This module contains enums required for testing."""
from enum import Enum


class HttpRequestMethod(Enum):
    """Enum class for indicating the http request method."""

    GET = 1
    """Http GET method"""
    POST = 2
    """Http POST method"""
