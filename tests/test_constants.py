"""Constant storage for test functions."""

# region HTTP STATUS CODES
from decimal import Decimal
from typing import Any

STATUS_METHOD_NOT_ALLOWED: int = 405
"""The request method is not supported by the target resource"""
STATUS_IM_A_TEAPOT: int = 418
"""Test for unknown error codes from server"""
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
TEST_URI_PATH: str = "/test/path/"
"""Test uri path"""
TEST_GET_MARGIN_ASSET_DETAILS_URI: str = "/r/margin/margin-account-v2/"
"""Test uri to get margin asset details"""
# endregion SERVER

# region CORRECT RESPONSES
TEST_URI_SUCCESS_CONTENT: str = '{"RESULT": "SUCCESS"}'
"""Success message for get method"""
EXPECTED_CORRECT_GET_RESPONSE_TEXT: dict[str, str] = {"RESULT": "SUCCESS"}
"""Expected response from get uri path"""
TEST_POST_CONTENT: str = "TEST_CONTENT"
"""Sample POST data content"""
GET_SYMBOL_DETAILS_RESPONSE_CONTENT: str = (
    '{"first_currency_credit":{"currency":{"name":"TEST_SYMBOL_NAME"},'
    '"pair":{"first_currency_precision":3,"price_precision":6}},'
    '"second_currency_credit":{"available_amount":"470.2352303"},'
    '"id": 123456789, "pair": {"id": 560}}'
)
"""Expected message for get_margin_asset_id"""
GET_SYMBOL_DETAILS_RESPONSE_DICTIONARY: dict[str, Any] = {
    "first_currency_credit": {
        "currency": {"name": "TEST_SYMBOL_NAME"},
        "pair": {"first_currency_precision": 3, "price_precision": 6},
    },
    "second_currency_credit": {"available_amount": "470.2352303"},
    "id": 123456789,
    "pair": {"id": 560},
}
TEST_ISOLATED_SYMBOL: str = "TESTUSDT"
"""Test isolated symbol"""
TEST_ISOLATED_SYMBOL_NAME: str = "TEST_SYMBOL_NAME"
"""Test isolated symbol name"""
TEST_MARGIN_ASSET_BALANCE: Decimal = Decimal("470.2352303")
"""Test asset balance"""
TEST_VOLUME_PRECISION: int = 3
"""Test asset volume ordering precision requirements"""
TEST_PRICE_PRECISION: int = 6
"""Test asset price ordering precision requirements"""
INVALID_ISOLATED_SYMBOL: str = "INVALIDUSDT"
"""Invalid isolated symbol"""
TEST_MARGIN_ASSET_ID: int = 123456789
"""Test margin asset ID"""
TEST_ISOLATED_MARGIN_MARKET_GENRE: str = "IsolatedMargin"
"""Test market genre for isolated margin"""
TEST_GET_ALL_MARGIN_OPEN_ORDERS_CONTENT: str = (
    '[{"id": 1, "break_even_point": "5578"}, {"id": 254, "break_even_point": "0.740"}]'
)
"""Success message for get all margin open orders method"""
GET_ALL_MARGIN_OPEN_ORDERS_TEST_RESPONSE_ITEM_COUNT: int = 2
"""Number of items in the test response for get all margin open orders function"""
TEST_ASSET_ID: int = 254
"""Test asset ID to retrieve information from get all margin open orders"""
TEST_BREAK_EVEN_PRICE: Decimal = Decimal("0.74")
"""Test break even price"""
TEST_MARGIN_PAIR_ID: int = 560
"""Test margin pair ID"""
# endregion CORRECT RESPONSES

# region INVALID RESPONSES
TEST_URI_FAILED_CONTENT: str = '{"RESULT": "FAILED"}'
"""Fail message for get method"""
ERROR_POST_DATA_TO_SERVER_RESPONSE: tuple[bool, None] = (False, None)
"""Fail response from post_data_to_server function"""
INVALID_POST_CONTENT: str = "INVALID_CONTENT"
"""Invalid POST data content"""
INVALID_ASSET_ID: int = 293876
# endregion INVALID RESPONSES

# region UTILITIES
SAMPLE_DECIMAL_INT_VERY_HIGH: int = 2592500000000000000000000000000000000000000000000000
"""Sample very high value as integer"""
SAMPLE_DECIMAL_STR_VERY_HIGH: str = "2.5925E+51"
"""Sample very high value as string"""
SAMPLE_DECIMAL_INT_HIGH: int = 375000000000000000000000
"""Sample high value as integer"""
SAMPLE_DECIMAL_STR_HIGH: str = "375000000000000000000000"
"""Sample high value as string"""
SAMPLE_DECIMAL_FLOAT_LOW: str = "0.0000000000002"
"""Sample low value as float"""
SAMPLE_DECIMAL_STR_LOW: str = "2E-13"
"""Sample low value as string"""
SAMPLE_DECIMAL_FLOAT_VERY_LOW: str = "0.00000000000000000000000000000000000000043235"
"""Sample very low value as float"""
SAMPLE_DECIMAL_STR_VERY_LOW: str = "4.3235E-40"
"""Sample very low value as string"""
SAMPLE_JSON_DATA: str = '{"markets":[{"spot_grid_bot_active":false,"market_id":1},{"market_id":2}]}'
"""Sample json data to process"""
# endregion UTILITIES
