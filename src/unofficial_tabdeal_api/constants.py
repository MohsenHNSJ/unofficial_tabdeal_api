"""Constants storage."""

BASE_API_URL: str = "https://api-web.tabdeal.org"

GET_ACCOUNT_PREFERENCES_URI: str = "/r/preferences/"
"""URL for getting account preferences. Used for checking authorization key validity"""

# region Server Statuses
STATUS_OK: int = 200
"""The request succeeded"""
STATUS_UNAUTHORIZED: int = 401
"""Authorization token is invalid or expired"""
STATUS_BAD_REQUEST: int = 400
"""The server could not understand the request."""
# endregion Server Statuses

# region Server Responses
MARKET_NOT_FOUND_RESPONSE: str = '{"error":"بازار یافت نشد."}'
"""Response when requested market is not found on Tabdeal"""
MARGIN_NOT_ACTIVE_RESPONSE: str = '{"error":"معامله‌ی اهرم‌دار فعال نیست."}'
"""Response when requested market is not available for margin trading on Tabdeal platform"""
NOT_ENOUGH_BALANCE_RESPONSE: str = '{"error":"اعتبار کافی نیست."}'
"""Response when asset balance is insufficient for requested order"""
# endregion Server Responses

# region Authorization
AUTH_KEY_INVALIDITY_THRESHOLD: int = 5
"""Number of consecutive fail responses to be tolerated,
before giving up in keep_authorization_key_alive"""
# endregion Authorization

# region Margin
GET_MARGIN_ASSET_DETAILS_PRT1: str = "/r/margin/margin-account-v2/?pair_symbol="
"""First part the URL for getting margin asset details
The isolated_symbol of the margin asset is added between the two parts"""
GET_MARGIN_ASSET_DETAILS_PRT2: str = "&account_genre=IsolatedMargin"
"""Seconds part of the URL for getting margin asset details
The isolated_symbol of the margin asset is added between the two parts"""
GET_ALL_MARGIN_OPEN_ORDERS_URI: str = "/r/treasury/isolated_positions/"
"""URL for getting all open margin orders."""
# endregion Margin

# region Utilities
DECIMAL_PRECISION: int = 10
"""Max decimal precision needed"""
# endregion Utilities
