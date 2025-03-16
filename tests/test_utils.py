"""This module is for testing the functions of utils module."""
# ruff: noqa: S101

from unofficial_tabdeal_api.utils import create_session_headers

TEST_USER_HASH: str = "TEST_USER_HASH"
TEST_USER_AUTH_KEY: str = "TEST_USER_AUTH_KEY"


def test_create_session_headers() -> None:
    """Tests the function of create_session_headers."""
    expected_result: dict[str, str] = {
        "user-hash": TEST_USER_HASH,
        "Authorization": TEST_USER_AUTH_KEY,
    }
    assert create_session_headers(
        TEST_USER_HASH, TEST_USER_AUTH_KEY) == expected_result
