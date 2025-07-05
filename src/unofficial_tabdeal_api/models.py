"""This module holds the data models for the API."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from unofficial_tabdeal_api.constants import MAX_ALLOWED_MARGIN_LEVEL
from unofficial_tabdeal_api.enums import OrderSide


# region Margin-related models
class MarginOrderModel(BaseModel):
    """This is the class storing information about a margin order."""

    isolated_symbol: str
    """Symbol of the order, e.g. BTCUSDT"""
    order_price: Decimal = Field(..., gt=0)
    """Price of the order, e.g. 10000.00"""
    order_side: OrderSide
    """Side of the order, either BUY or SELL"""
    margin_level: Decimal = Field(..., gt=0, le=MAX_ALLOWED_MARGIN_LEVEL)
    """Margin level of the order,
    Must be greater than 0 and less than or equal to MAX_ALLOWED_MARGIN_LEVEL"""
    deposit_amount: Decimal = Field(..., gt=0)
    """Deposit amount for the order, e.g. 1000.00"""
    stop_loss_percent: Decimal = Field(..., ge=0)
    """Percentile of tolerate-able loss, e.g. 5 for 5%"""
    take_profit_percent: Decimal = Field(..., ge=0)
    """Percentile of expected profit, e.g. 10 for 10%"""
    volume_fraction_allowed: bool
    """Whether volume fraction is allowed, e.g. True or False"""
    volume_precision: int = 0
    """Precision of the volume, Defaults to 0"""


# endregion Margin-related models

# region Wallet-related models


class TransferFromMarginModel(BaseModel):
    """Model for transferring USDT from margin asset."""

    transfer_direction: str = "Out"
    """Direction of transfer, e.g. 'Out' for transferring out of margin asset."""
    amount: Decimal = Field(..., ge=0)
    """Amount to transfer, must be a positive decimal value."""
    currency_symbol: str = "USDT"
    """Currency symbol for the transfer, defaults to 'USDT'."""
    account_genre: str = "IsolatedMargin"
    """Genre of the account, e.g. 'IsolatedMargin', 'Spot', ..."""
    other_account_genre: str = "Main"
    """Genre of the other account, e.g. 'Main'."""
    pair_symbol: str
    """Symbol of the trading pair, e.g. 'BTCUSDT'."""


class TransferToMarginModel(BaseModel):
    """Model for transferring USDT to margin asset."""

    amount: int = 0
    """Amount to transfer, must be a positive integer value."""
    currency_symbol: str = "USDT"
    """Currency symbol for the transfer, defaults to 'USDT'."""
    transfer_amount_from_main: Decimal = Field(..., ge=0)
    """Amount to transfer from main account, must be a positive decimal value."""
    pair_symbol: str
    """Symbol of the trading pair, e.g. 'BTCUSDT'."""


class WalletDetailsModel(BaseModel):
    """Model for wallet details."""

    tether_us: Decimal = Field(
        ...,
        ge=0,
        alias="TetherUS",
    )
    """Amount of Tether US in the wallet, must be a positive decimal value."""

    model_config = ConfigDict(
        # Allows using either the field name (tether_us) or the alias ("TetherUS") when creating
        # or exporting the model.
        populate_by_name=True,
        # Allows extra fields in the input data that are not explicitly defined in the model.
        # This is useful for API responses that may include additional fields.
        extra="allow",
    )


# endregion Wallet-related models
