"""This module holds the data models for the API."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from unofficial_tabdeal_api.constants import MAX_ALLOWED_MARGIN_LEVEL
from unofficial_tabdeal_api.enums import OrderSide


# region Margin-related models
# region Base models
class PairModel(BaseModel):
    """Model for the isolated symbol pair details."""

    base_precision_visible: int
    """Precision of the base currency visible to user, e.g. 8"""
    first_currency_precision: int
    """Precision of the first currency, e.g. 8"""
    id: int
    """Pair ID"""
    last_trade_price: Decimal
    """NOT YET KNOWN"""
    price_precision: int
    """Precision of the price, e.g. 2"""
    quote_precision_visible: int
    """Precision of the quote currency visible to user, e.g. 2"""
    representation_name: str
    """Representation name of the pair, e.g. بیت‌ کوین-تتر"""
    symbol: str
    """Symbol of the pair, e.g. BTC_USDT"""
    symbol_fa: str
    """Symbol in Persian, e.g. بیت‌ کوین-تتر"""


class TriggerPriceModel(BaseModel):
    """Model for the trigger price details."""

    sl_price: Decimal | None = None
    """Stop Loss price, e.g. 9500.00"""
    tp_price: Decimal | None = None
    """Take Profit price, e.g. 10500.00"""


class CurrencyModel(BaseModel):
    """Model for the currency details."""

    id: int | None = None
    """ID of the currency.

    server MAY NOT SEND this property in some requests, Therefore,
    it defaults to `None` if not provided

    AVAILABLE: `get_margin_all_open_orders`

    NOT AVAILABLE: `get_isolated_symbol_details`"""
    name: str
    """Name of the currency, e.g. 'TetherUS'"""
    name_fa: str
    """Name of the currency in Persian, e.g. 'تتر'"""
    precision: int | None = None
    """Precision of the currency, e.g. 8.

    server MAY NOT SEND this property in some requests, Therefore, it defaults to `None`
     if not provided.

    AVAILABLE: `get_margin_all_open_orders`

    NOT AVAILABLE: `get_isolated_symbol_details`"""
    representation_name: str
    """Representation name of the currency, e.g. 'تتر'"""
    symbol: str
    """Symbol of the currency, e.g. 'USDT'"""


class CurrencyCreditModel(BaseModel):
    """Model for the currency credit details."""

    amount: Decimal
    """Total amount of the currency, e.g. 1100.00"""
    available_amount: Decimal
    """Available amount of the currency, e.g. 1000.00"""
    average_entry_price: Decimal
    """Average entry price of the currency, e.g. 10000.00"""
    borrow: Decimal
    """NOT YET KNOWN"""
    currency: CurrencyModel
    """Currency details of the credit"""
    frozen_amount: Decimal
    """Frozen amount of the currency, e.g. 100.00"""
    genre: str | None = None
    """Genre of the currency, e.g. 'IsolatedMargin'

    server MAY NOT SEND this property in some requests, Therefore,
    it defaults to `None` if not provided

    AVAILABLE: `get_isolated_symbol_details`

    NOT AVAILABLE: `get_margin_all_open_orders`"""
    genre_fa: str | None = None
    """Genre of the currency in Persian, e.g. 'کیف پول معامله اهرم‌دار Isolated'

    server MAY NOT SEND this property in some requests, Therefore,
    it defaults to `None` if not provided

    AVAILABLE: `get_isolated_symbol_details`

    NOT AVAILABLE: `get_margin_all_open_orders`"""
    interest: Decimal
    """Interest on the currency, e.g. 10.00"""
    irt_average_entry_price: Decimal
    """Average entry price of the currency in IRT, e.g. 100000000.00"""
    irt_value: Decimal
    """Amount of credit in symbol as IRT, e.g. 10000000.00"""
    is_borrowable: bool
    """Whether the currency is borrowable, e.g. True or False"""
    max_transfer_out_amount: Decimal | None = None
    """Max amount of the currency that can be transferred out, e.g. 900.00

    server MAY NOT SEND this property in some requests, Therefore,
    it defaults to `None` if not provided

    AVAILABLE: `get_isolated_symbol_details`

    NOT AVAILABLE: `get_margin_all_open_orders`"""
    pair: PairModel | None = None
    """Pair details of the credit

    server MAY NOT SEND this property in some requests, Therefore,
    it defaults to `None` if not provided

    AVAILABLE: `get_isolated_symbol_details`

    NOT AVAILABLE: `get_margin_all_open_orders`"""
    position: Decimal
    """NOT YET KNOWN"""
    position_usdt_value: Decimal | None = None
    """Value of the position as USDT. For example, 93427.9345

    server MAY NOT SEND this property in some requests, Therefore, it defaults to `None`
    if not provided.

    AVAILABLE: `get_margin_all_open_orders`

    NOT AVAILABLE: `get_isolated_symbol_details`"""
    position_irt_value: Decimal | None = None
    """Value of the position as IRT. For example, 3255.787

    server MAY NOT SEND this property in some requests, Therefore, it defaults to `None`
    if not provided.

    AVAILABLE: `get_margin_all_open_orders`

    NOT AVAILABLE: `get_isolated_symbol_details`"""
    position_value: Decimal
    """NOT YET KNOWN"""
    usdt_value: Decimal
    """Amount of credit in symbol as USDT, e.g. 1000.00"""


# endregion Base models


class IsolatedSymbolDetailsModel(BaseModel):
    """Model for isolated symbol details."""

    active: bool
    """Whether the isolated symbol is active for trading, e.g. True or False"""
    borrow_active: bool
    """Whether the isolated symbol is active for borrowing credit, e.g. True or False"""
    break_even_point: Decimal
    """Break-even point for the isolated symbol, e.g. 10000.00
    This is the point where the profit/loss is zero."""
    first_currency_borrowable_amount: Decimal
    """Borrowable amount of the first currency, e.g. 1000.00"""
    first_currency_credit: CurrencyCreditModel
    """Currency details of first symbol."""
    id: int
    """ID of the isolated symbol market, e.g. 157092"""
    margin_active: bool
    """Whether the isolated symbol is active for margin trading, e.g. True or False"""
    max_margin_level: Decimal = Field(..., alias="max_leverage")
    """Max margin level for the isolated symbol, e.g. 60.0
    This is defined by symbol and user trading amount"""
    pair: PairModel
    """Isolated symbol pair details."""
    second_currency_borrowable_amount: Decimal
    """Borrowable amount of the second currency, e.g. 1000.00"""
    second_currency_credit: CurrencyCreditModel
    """Currency details of second symbol, for example, USDT in BTCUSDT"""
    trader: int
    """ID of the trader, e.g. 5403"""
    transfer_active: bool
    """Whether the isolated symbol is active for transferring credit, e.g. True or False"""
    trigger_price: TriggerPriceModel
    """User-set trigger price points for Stop loss and Take profit."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class MarginOpenOrderModel(BaseModel):
    """Model for open margin orders."""

    break_even_point: Decimal
    """Break-even point for the isolated symbol, e.g. 10000.00
    This is the point where the profit/loss is zero."""
    first_currency_credit: CurrencyCreditModel
    """Currency details of first symbol, for example, BTC in BTCUSDT"""
    id: int
    """ID of the isolated symbol market. for example, 157092."""
    is_long: bool = Field(..., alias="isLong")
    """Whether the order is Long(True) or not (Short = False)"""
    is_order_filled: bool = Field(..., alias="isOrderFilled")
    """Whether the order is filled completely(True) or not(False)"""
    pair: PairModel
    """Isolated symbol pair details."""
    risk_name: str
    """Amount of risk in string, determined by server. For example, 'Moderate'"""
    second_currency_credit: CurrencyCreditModel
    """Currency details of second symbol, for example, USDT in BTCUSDT"""
    trigger_price: TriggerPriceModel
    """User-set trigger price points for Stop loss and Take profit."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")


# endregion Margin-related models

# region Order-related models


class MarginOrderModel(BaseModel):
    """This is the class storing information about a margin order."""

    deposit_amount: Decimal = Field(..., gt=0)
    """Deposit amount for the order, e.g. 1000.00"""
    isolated_symbol: str
    """Symbol of the order, e.g. BTCUSDT"""
    margin_level: Decimal = Field(..., gt=0, le=MAX_ALLOWED_MARGIN_LEVEL)
    """Margin level of the order,
    Must be greater than 0 and less than or equal to MAX_ALLOWED_MARGIN_LEVEL"""
    order_price: Decimal = Field(..., gt=0)
    """Price of the order, e.g. 10000.00"""
    order_side: OrderSide
    """Side of the order, either BUY or SELL"""
    stop_loss_percent: Decimal = Field(..., ge=0)
    """Percentile of tolerate-able loss, e.g. 5 for 5%"""
    take_profit_percent: Decimal = Field(..., ge=0)
    """Percentile of expected profit, e.g. 10 for 10%"""
    volume_fraction_allowed: bool
    """Whether volume fraction is allowed, e.g. True or False"""
    volume_precision: int = 0
    """Precision of the volume, Defaults to 0"""


# endregion Order-related models

# region Wallet-related models


class TransferFromMarginModel(BaseModel):
    """Model for transferring USDT from margin asset."""

    account_genre: str = "IsolatedMargin"
    """Genre of the account, e.g. 'IsolatedMargin', 'Spot', ..."""
    amount: Decimal = Field(..., ge=0)
    """Amount to transfer, must be a positive decimal value."""
    currency_symbol: str = "USDT"
    """Currency symbol for the transfer, defaults to 'USDT'."""
    other_account_genre: str = "Main"
    """Genre of the other account, e.g. 'Main'."""
    pair_symbol: str
    """Symbol of the trading pair, e.g. 'BTCUSDT'."""
    transfer_direction: str = "Out"
    """Direction of transfer, e.g. 'Out' for transferring out of margin asset."""


class TransferToMarginModel(BaseModel):
    """Model for transferring USDT to margin asset."""

    amount: int = 0
    """A default value that is always 0 for no reason."""
    currency_symbol: str = "USDT"
    """Currency symbol for the transfer, defaults to 'USDT'."""
    pair_symbol: str
    """Symbol of the trading pair, e.g. 'BTCUSDT'."""
    transfer_amount_from_main: Decimal = Field(..., ge=0)
    """Amount to transfer from main account, must be a positive decimal value."""


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
