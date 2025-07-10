"""Constants storage."""

from decimal import Decimal
from typing import Any

BASE_API_URL: str = "https://api-web.tabdeal.org"
TEST_SERVER_URL: str = "http://127.0.0.1:32000"

GET_ACCOUNT_PREFERENCES_URI: str = "/r/preferences/"
"""URL for getting account preferences. Used for checking authorization key validity"""

# region Server Statuses
STATUS_OK: int = 200
"""The request succeeded"""
STATUS_UNAUTHORIZED: int = 401
"""Authorization token is invalid or expired"""
STATUS_BAD_REQUEST: int = 400
"""The server could not understand the request."""
STATUS_NOT_FOUND: int = 404
"""The requested resource could not be found but may be available in the future."""
# endregion Server Statuses

# region Server Responses
MARKET_NOT_FOUND_RESPONSE: str = '{"error":"بازار یافت نشد."}'
"""Response when requested market is not found on Tabdeal"""
MARGIN_NOT_ACTIVE_RESPONSE: str = '{"error":"معامله‌ی اهرم‌دار فعال نیست."}'
"""Response when requested market is not available for margin trading on Tabdeal platform"""
NOT_ENOUGH_BALANCE_RESPONSE: str = '{"error":"اعتبار کافی نیست."}'
"""Response when asset balance is insufficient for requested order"""
NOT_ENOUGH_CREDIT_AVAILABLE_RESPONSE: str = '{"error":"شما به سقف دریافت اعتبار رسیده‌اید."}'
"""Response when requested borrow amount is over available credit"""
ORDER_PLACED_SUCCESSFULLY_RESPONSE: str = "سفارش با موفقیت ثبت شد."
"""Response when order is successfully placed"""
REQUESTED_PARAMETERS_INVALID_RESPONSE: str = '{"error":"پارامتر های ورود اشتباه است."}'
"""Response when requested parameters are invalid"""
ORDER_IS_INVALID_RESPONSE: str = '{"error":"نوع سفارش اشتباه است."}'
"""Response when order type is invalid"""
TRANSFER_AMOUNT_OVER_ACCOUNT_BALANCE_RESPONSE: str = (
    '{"error":"مقدار واردشده، بیش از حداکثر مقدار قابل جابه‌جایی است."}'
)
"""Response when requested transfer amount is over the account available balance"""
TRANSFER_FROM_MARGIN_ASSET_TO_WALLET_NOT_POSSIBLE_RESPONSE: str = (
    '{"error":"امکان انتقال ارز به خارج اکانت معامله اهرم‌دار، امکان‌پذیر نیست."}'
)
"""Response when for some unknown reason,
It's not possible to transfer USDT out of margin asset"""
MARGIN_POSITION_NOT_FOUND_RESPONSE: str = '{"error":"پوزیشن مورد نظر یافت نشد."}'
"""Response when server can't set SL/TP for margin order due to unknown error"""
GENERIC_SERVER_CONFIRMATION_RESPONSE: str = '"درخواست مورد نظر با موفقیت انجام شد."'
"""Response when server receives the request, no guarantee of actually processing it!!!"""
# endregion Server Responses

# region Authorization
AUTH_KEY_INVALIDITY_THRESHOLD: int = 5
"""Number of consecutive fail responses to be tolerated,
before giving up in keep_authorization_key_alive"""
# endregion Authorization

# region Margin
GET_MARGIN_ASSET_DETAILS_URI: str = "/r/margin/margin-account-v2/"
"""URL for getting margin asset details"""
GET_ALL_MARGIN_OPEN_ORDERS_URI: str = "/r/treasury/isolated_positions/"
"""URL for getting all open margin orders."""
OPEN_MARGIN_ORDER_URI: str = "/api/order/"
"""URL for opening a margin order"""
MAX_ALLOWED_MARGIN_LEVEL: Decimal = Decimal("60.0")
"""Max allowed margin level for margin orders"""
# endregion Margin

# region Order
GET_ORDERS_HISTORY_URI: str = "/r/api/user_order/"
"""URL for getting all orders history"""
# endregion Order

# region Wallet
GET_WALLET_USDT_BALANCE_URI: str = "/r/api/user/"
"""URL for getting the USDT balance of account"""
GET_WALLET_USDT_BALANCE_QUERY: dict[str, Any] = {"market_id": 3}
"""QUERY for getting the USDT balance of account"""
TRANSFER_USDT_TO_MARGIN_ASSET_URI: str = "/margin/other-margins-transfer/"
"""URL for transferring USDT from wallet to margin asset"""
TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_URI: str = "/margin/transfer/"
"""URL for transferring USDT from margin asset to wallet"""
SET_SL_TP_FOR_MARGIN_ORDER_URI: str = "/margin/margin-trigger-price/"
"""URL for setting stop loss and take profit points for a margin order"""
# endregion Wallet

# region Utilities
DECIMAL_PRECISION: int = 20
"""Max decimal precision needed"""
REQUIRED_USDT_PRECISION: int = 8
"""Precision needed for USDT"""
# endregion Utilities
