"""This module is for testing the functions of utils module."""
# ruff: noqa: S101

from unofficial_tabdeal_api.utils import create_session_headers

TEST_USER_HASH: str = "TEST_USER_HASH"
TEST_USER_AUTH_KEY: str = "TEST_USER_AUTH_KEY"

# region Expected_results
expected_session_headers: dict[str, str] = {
    "user-hash": TEST_USER_HASH,
    "Authorization": TEST_USER_AUTH_KEY,
}
# endregion Expected_results


async def test_create_session_headers_async() -> None:
    """Tests the function of create_session_headers."""
    result = create_session_headers(TEST_USER_HASH, TEST_USER_AUTH_KEY)
    assert result == expected_session_headers
