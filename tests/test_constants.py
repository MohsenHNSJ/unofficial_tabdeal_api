"""Constant storage for test functions."""

# region HTTP STATUS CODES
STATUS_OK: int = 200
"""The request succeeded"""
STATUS_BAD_REQUEST: int = 400
"""The server cannot not process the request due to client error"""
STATUS_UNAUTHORIZED: int = 401
"""The client must authenticate itself to get the requested response"""
STATUS_METHOD_NOT_ALLOWED: int = 405
"""The request method is not supported by the target resource"""
# endregion HTTP STATUS CODES

# region SESSION
TEST_USER_HASH: str = "TEST_USER_HASH"
"""Sample correct user hash"""
TEST_USER_AUTH_KEY: str = "TEST_USER_AUTH_KEY"
"""Sample correct user authorization key"""
EXPECTED_SESSION_HEADERS: dict[str, str] = {
    "user-hash": TEST_USER_HASH,
    "Authorization": TEST_USER_AUTH_KEY,
}
"""Session header expected to receive"""
INVALID_USER_HASH: str = "INVALID_USER_HASH"
"""Sample invalid user hash"""
INVALID_USER_AUTH_KEY: str = "INVALID_USER_AUTH_KEY"
"""Sample invalid user authorization key"""
# endregion SESSION

# region SERVER
TEST_SERVER_PORT: int = 32000
"""Specified port to be used by test server"""
TEST_SERVER_ADDRESS: str = f"http://127.0.0.1:{TEST_SERVER_PORT}"
"""Address of test server to be used as base_url for ClientSession"""
INVALID_SERVER_ADDRESS: str = "http://127.0.0.2:4030"
"""Address of an invalid server for exception testing"""
TEST_URI_PATH: str = "/test/path/"
"""Test uri path"""
TEST_GET_ALL_MARGIN_OPEN_ORDERS_URI: str = "/r/treasury/isolated_positions/"
"""Test uri path for getting all margin open orders"""
# endregion SERVER

# region CORRECT RESPONSES
TEST_URI_SUCCESS_CONTENT: str = '{"RESULT": "SUCCESS"}'
"""Success message for get method"""
EXPECTED_CORRECT_GET_RESPONSE_TEXT: dict[str, str] = {"RESULT": "SUCCESS"}
"""Expected response from get uri path"""
TEST_POST_CONTENT: str = "TEST_CONTENT"
"""Sample POST data content"""
TEST_GET_MARGIN_ASSET_ID: str = '{"id": 123456789}'
"""Expected message for get_margin_asset_id"""
TEST_ISOLATED_SYMBOL: str = "TESTUSDT"
"""Test isolated symbol"""
TEST_MARGIN_ASSET_ID: int = 123456789
"""Test margin asset ID"""
TEST_ISOLATED_MARGIN_MARKET_GENRE: str = "IsolatedMargin"
"""Test market genre for isolated margin"""
TEST_GET_ALL_MARGIN_OPEN_ORDERS_CONTENT: str = '[{"id": 1, "num": "5"}, {"id": 2, "num": "2"}]'
"""Success message for get all margin open orders method"""
GET_ALL_MARGIN_OPEN_ORDERS_TEST_RESPONSE_ITEM_COUNT: int = 2
"""Number of items in the test response for get all margin open orders function"""
# endregion CORRECT RESPONSES

# region INVALID RESPONSES
TEST_URI_FAILED_CONTENT: str = '{"RESULT": "FAILED"}'
"""Fail message for get method"""
ERROR_POST_DATA_TO_SERVER_RESPONSE: tuple[bool, None] = (False, None)
"""Fail response from post_data_to_server function"""
INVALID_POST_CONTENT: str = "INVALID_CONTENT"
"""Invalid POST data content"""
# endregion INVALID RESPONSES
