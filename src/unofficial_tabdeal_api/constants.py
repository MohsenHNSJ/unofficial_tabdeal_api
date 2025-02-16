"""Constants storage"""

GET_ACCOUNT_PREFERENCES_URL: str = "https://api.etctabdeal.org/r/preferences/"
"""URL for getting account preferences. Used for checking authorization key validity"""

# region Margin
GET_MARGIN_ASSET_DETAILS_PRT1: str = (
    "https://api.etctabdeal.org/margin/margin-account-v2/?pair_symbol="
)
"""First part the URL for getting margin asset details
The isolated_symbol of the margin asset is added between the two parts"""
GET_MARGIN_ASSET_DETAILS_PRT2: str = "&account_genre=IsolatedMargin"
"""Seconds part of the URL for getting margin asset details
The isolated_symbol of the margin asset is added between the two parts"""
GET_ALL_MARGIN_OPEN_ORDERS_URL: str = (
    "https://api.etctabdeal.org/r/treasury/isolated_positions/"
)
"""URL for getting all open margin orders."""
# endregion Margin
