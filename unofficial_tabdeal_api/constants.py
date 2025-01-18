"""Stores constant variables"""

GET_MARGIN_ASSET_DETAILS_PRT1: str = (
    "https://api.etctabdeal.org/margin/margin-account-v2/?pair_symbol="
)
"""First part the URL for getting margin asset details
The isolated_symbol of the margin asset is added between the two parts"""
GET_MARGIN_ASSET_DETAILS_PRT2: str = "&account_genre=IsolatedMargin"
"""Seconds part of the URL for getting margin asset details
The isolated_symbol of the margin asset is added between the two parts"""
