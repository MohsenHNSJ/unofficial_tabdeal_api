"""This module is for testing the functions of utils module."""
# ruff: noqa: S101

from tests.test_constants import EXPECTED_SESSION_HEADERS, TEST_USER_AUTH_KEY, TEST_USER_HASH
from unofficial_tabdeal_api.utils import create_session_headers


def test_create_session_headers() -> None:
    """Tests the function of create_session_headers."""
    # Create session headers using test data
    result = create_session_headers(TEST_USER_HASH, TEST_USER_AUTH_KEY)
    # Check if received data is as expected
    assert result == EXPECTED_SESSION_HEADERS
