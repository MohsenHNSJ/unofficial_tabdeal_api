"""Constant storage for test functions."""
STATUS_OK: int = 200
"""The request succeeded"""
STATUS_BAD_REQUEST: int = 400
"""The server cannot not process the request due to client error"""
STATUS_UNAUTHORIZED: int = 401
"""The client must authenticate itself to get the requested response"""
STATUS_METHOD_NOT_ALLOWED: int = 405
"""The request method is not supported by the target resource"""

TEST_USER_HASH: str = "TEST_USER_HASH"
"""Sample user hash"""
TEST_USER_AUTH_KEY: str = "TEST_USER_AUTH_KEY"
"""Sample user authorization key"""
EXPECTED_SESSION_HEADERS: dict[str, str] = {
    "user-hash": TEST_USER_HASH,
    "Authorization": TEST_USER_AUTH_KEY,
}
"""Session header expected to receive"""

TEST_SERVER_PORT: int = 32000
"""Specified port to be used by test server"""
TEST_SERVER_ADDRESS: str = f"http://127.0.0.1:{TEST_SERVER_PORT}"
"""Address of test server to be used as base_url for ClientSession"""

TEST_URI_PATH: str = "/test/path/"
"""Test uri path"""
TEST_URI_SUCCESS_CONTENT: str = '{"RESULT": "SUCCESS"}'
"""Success message for get method"""
TEST_URI_FAILED_CONTENT: str = '{"RESULT": "FAILED"}'
"""Fail message for get method"""
EXPECTED_TEST_GET_RESPONSE_TEXT: dict[str, str] = {"RESULT": "SUCCESS"}
"""Expected response from get uri path"""
TEST_POST_CONTENT: str = "TEST_CONTENT"
