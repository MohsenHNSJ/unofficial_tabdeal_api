"""Constant storage for test functions."""
# ruff: noqa: E501
# pylint: disable=W0105,C0301

from decimal import Decimal
from typing import Any

from unofficial_tabdeal_api.enums import OrderSide
from unofficial_tabdeal_api.models import (
    CurrencyCreditModel,
    CurrencyModel,
    IsolatedSymbolDetailsModel,
    MarginOpenOrderModel,
    MarginOrderModel,
    PairModel,
    TriggerPriceModel,
)

# region HTTP STATUS CODES
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

# region SERVER DETAILS
TEST_SERVER_PORT: int = 32000
"""Specified port to be used by test server"""
TEST_SERVER_ADDRESS: str = f"http://127.0.0.1:{TEST_SERVER_PORT}"
"""Address of test server to be used as base_url for ClientSession"""
TEST_URI_PATH: str = "/test/path/"
"""Test uri path"""
UNKNOWN_URI_PATH: str = "/unknown/path/"
"""Unknown uri path to test error handling"""
USER_UNAUTHORIZED_RESPONSE: str = '{"detail":"Token is invalid or expired"}'
"""User unauthorized response from server"""
# endregion SERVER DETAILS

# region CORRECT RESPONSES
# Base values
SAMPLE_AMOUNT: Decimal = Decimal("140.5")
"""Sample amount value"""
SAMPLE_BREAK_EVEN_PRICE: Decimal = Decimal("96967.5034")
"""Sample break even price"""
SAMPLE_BREAK_EVEN_PRICE_2: Decimal = Decimal("60.47")
"""Sample break even price"""
SAMPLE_BREAK_EVEN_PRICE_3: Decimal = Decimal("0.00000001")
"""Sample break even price"""
SAMPLE_GENRE: str = "IsolatedMargin"
"""Sample genre value"""
SAMPLE_GENRE_PERSIAN: str = "کیف پول معامله اهرم دار"
"""Sample genre value in Persian"""
SAMPLE_ID: int = 170
"""Sample currency ID"""
SAMPLE_ID_2: int = 96503
"""Sample currency ID"""
SAMPLE_ID_3: int = 777777
"""Sample currency ID"""
SAMPLE_PRECISION: int = 6
"""Sample precision value"""
SAMPLE_PRECISION_2: int = 4
"""Sample precision value"""
SAMPLE_PRECISION_3: int = 8
"""Sample precision value"""
SAMPLE_PRICE: Decimal = Decimal("23562.23")
"""Sample price value"""
SAMPLE_PRICE_2: Decimal = Decimal(value="0.3452")
"""Sample price value"""
SAMPLE_PRICE_3: Decimal = Decimal(value="0.00000001")
"""Sample price value"""
SAMPLE_RISK_NAME: str = "Moderate"
"""Sample risk name"""
SAMPLE_STOP_LOSS_PRICE: Decimal = Decimal("270.540")
"""Sample stop loss price"""
SAMPLE_SYMBOL_NAME: str = "TESTUSDT"
"""Sample symbol name"""
SAMPLE_SYMBOL_NAME_2: str = "TESTBTC"
"""Sample symbol name"""
SAMPLE_SYMBOL_NAME_3: str = "UNTRADEUSDT"
"""Sample symbol name"""
SAMPLE_SYMBOL_FULL_NAME: str = "TESTUSDT - TEST-DOLLAR"
"""Sample full symbol name"""
SAMPLE_SYMBOL_FULL_NAME_2: str = "TESTBTC - TEST-BITCOIN"
"""Sample full symbol name"""
SAMPLE_SYMBOL_FULL_NAME_3: str = "UNTRADEUSDT - UN-TRADEABLE-DOLLAR"
"""Sample full symbol name"""
SAMPLE_SYMBOL_PERSIAN_NAME: str = "تست-دلار"
"""Sample symbol name in Persian"""
SAMPLE_SYMBOL_PERSIAN_NAME_2: str = "تست-بیت‌کوین"
"""Sample symbol name in Persian"""
SAMPLE_SYMBOL_PERSIAN_NAME_3: str = "تست-دلار-غیرفعال"
"""Sample symbol name in Persian"""
SAMPLE_TAKE_PROFIT_PRICE: Decimal = Decimal("219.080")
"""Sample take profit price"""

# Get symbol details section
SAMPLE_TRIGGER_PRICE_MODEL: TriggerPriceModel = TriggerPriceModel(
    sl_price=SAMPLE_STOP_LOSS_PRICE,
    tp_price=SAMPLE_TAKE_PROFIT_PRICE,
)
"""Sample trigger price model"""
SAMPLE_CURRENCY_MODEL: CurrencyModel = CurrencyModel(
    id=SAMPLE_ID,
    name=SAMPLE_SYMBOL_NAME,
    name_fa=SAMPLE_SYMBOL_PERSIAN_NAME,
    precision=SAMPLE_PRECISION,
    representation_name=SAMPLE_SYMBOL_FULL_NAME,
    symbol=SAMPLE_SYMBOL_NAME,
)
"""Sample currency model"""
SAMPLE_CURRENCY_MODEL_2: CurrencyModel = CurrencyModel(
    id=SAMPLE_ID_2,
    name=SAMPLE_SYMBOL_NAME_2,
    name_fa=SAMPLE_SYMBOL_PERSIAN_NAME_2,
    precision=SAMPLE_PRECISION_2,
    representation_name=SAMPLE_SYMBOL_FULL_NAME_2,
    symbol=SAMPLE_SYMBOL_NAME_2,
)
"""Sample currency model"""
SAMPLE_CURRENCY_MODEL_3: CurrencyModel = CurrencyModel(
    id=SAMPLE_ID_3,
    name=SAMPLE_SYMBOL_NAME_3,
    name_fa=SAMPLE_SYMBOL_PERSIAN_NAME_3,
    precision=SAMPLE_PRECISION_3,
    representation_name=SAMPLE_SYMBOL_FULL_NAME_3,
    symbol=SAMPLE_SYMBOL_NAME_3,
)
"""Sample currency model"""
SAMPLE_PAIR_MODEL: PairModel = PairModel(
    base_precision_visible=SAMPLE_PRECISION,
    first_currency_precision=SAMPLE_PRECISION_2,
    id=SAMPLE_ID,
    last_trade_price=SAMPLE_PRICE,
    price_precision=SAMPLE_PRECISION,
    quote_precision_visible=SAMPLE_PRECISION_2,
    representation_name=SAMPLE_SYMBOL_FULL_NAME,
    symbol=SAMPLE_SYMBOL_FULL_NAME,
    symbol_fa=SAMPLE_SYMBOL_PERSIAN_NAME,
)
"""Sample pair model"""
SAMPLE_PAIR_MODEL_2: PairModel = PairModel(
    base_precision_visible=SAMPLE_PRECISION,
    first_currency_precision=SAMPLE_PRECISION_2,
    id=SAMPLE_ID_2,
    last_trade_price=SAMPLE_PRICE,
    price_precision=SAMPLE_PRECISION,
    quote_precision_visible=SAMPLE_PRECISION_2,
    representation_name=SAMPLE_SYMBOL_FULL_NAME_2,
    symbol=SAMPLE_SYMBOL_FULL_NAME_2,
    symbol_fa=SAMPLE_SYMBOL_PERSIAN_NAME_2,
)
"""Sample pair model"""
SAMPLE_PAIR_MODEL_3: PairModel = PairModel(
    base_precision_visible=SAMPLE_PRECISION_3,
    first_currency_precision=SAMPLE_PRECISION_3,
    id=SAMPLE_ID_3,
    last_trade_price=SAMPLE_PRICE,
    price_precision=SAMPLE_PRECISION_3,
    quote_precision_visible=SAMPLE_PRECISION_3,
    representation_name=SAMPLE_SYMBOL_FULL_NAME_3,
    symbol=SAMPLE_SYMBOL_FULL_NAME_3,
    symbol_fa=SAMPLE_SYMBOL_PERSIAN_NAME_3,
)
"""Sample pair model"""
SAMPLE_CURRENCY_CREDIT_MODEL: CurrencyCreditModel = CurrencyCreditModel(
    amount=SAMPLE_AMOUNT,
    available_amount=SAMPLE_AMOUNT,
    average_entry_price=SAMPLE_PRICE_2,
    borrow=SAMPLE_AMOUNT,
    currency=SAMPLE_CURRENCY_MODEL,
    frozen_amount=Decimal(0),
    genre=SAMPLE_GENRE,
    genre_fa=SAMPLE_GENRE_PERSIAN,
    interest=Decimal(
        "1.2",
    ),
    irt_average_entry_price=SAMPLE_PRICE_2,
    irt_value=Decimal(
        "1000.99",
    ),
    is_borrowable=True,
    max_transfer_out_amount=Decimal(
        "1000.00",
    ),
    pair=SAMPLE_PAIR_MODEL,
    position=Decimal(
        "9533.2",
    ),
    position_usdt_value=Decimal(
        "8562.23",
    ),
    position_irt_value=Decimal(
        "734.44",
    ),
    position_value=Decimal(
        "562.23",
    ),
    usdt_value=Decimal("62.83"),
)
"""Sample first currency credit model"""
SAMPLE_CURRENCY_CREDIT_MODEL_2: CurrencyCreditModel = CurrencyCreditModel(
    amount=SAMPLE_AMOUNT,
    available_amount=SAMPLE_AMOUNT,
    average_entry_price=SAMPLE_PRICE_2,
    borrow=SAMPLE_AMOUNT,
    currency=SAMPLE_CURRENCY_MODEL_2,
    frozen_amount=Decimal(0),
    genre=SAMPLE_GENRE,
    genre_fa=SAMPLE_GENRE_PERSIAN,
    interest=Decimal(
        "1.2",
    ),
    irt_average_entry_price=SAMPLE_PRICE_2,
    irt_value=Decimal(
        "1000.99",
    ),
    is_borrowable=True,
    max_transfer_out_amount=Decimal(
        "1000.00",
    ),
    pair=SAMPLE_PAIR_MODEL_2,
    position=Decimal(
        "9533.2",
    ),
    position_usdt_value=Decimal(
        "8562.23",
    ),
    position_irt_value=Decimal(
        "734.44",
    ),
    position_value=Decimal(
        "562.23",
    ),
    usdt_value=Decimal("62.83"),
)
"""Sample first currency credit model"""
SAMPLE_CURRENCY_CREDIT_MODEL_3: CurrencyCreditModel = CurrencyCreditModel(
    amount=SAMPLE_AMOUNT,
    available_amount=SAMPLE_AMOUNT,
    average_entry_price=SAMPLE_PRICE_3,
    borrow=SAMPLE_AMOUNT,
    currency=SAMPLE_CURRENCY_MODEL_3,
    frozen_amount=Decimal(0),
    genre=SAMPLE_GENRE,
    genre_fa=SAMPLE_GENRE_PERSIAN,
    interest=Decimal(
        "1.2",
    ),
    irt_average_entry_price=SAMPLE_PRICE_3,
    irt_value=Decimal(
        "1000.99",
    ),
    is_borrowable=True,
    max_transfer_out_amount=Decimal(
        "1000.00",
    ),
    pair=SAMPLE_PAIR_MODEL_2,
    position=Decimal(
        "9533.2",
    ),
    position_usdt_value=Decimal(
        "8562.23",
    ),
    position_irt_value=Decimal(
        "734.44",
    ),
    position_value=Decimal(
        "562.23",
    ),
    usdt_value=Decimal("62.83"),
)
"""Sample first currency credit model"""
GET_SYMBOL_DETAILS_SAMPLE_RESPONSE: IsolatedSymbolDetailsModel = IsolatedSymbolDetailsModel(
    active=True,
    borrow_active=True,
    break_even_point=SAMPLE_BREAK_EVEN_PRICE,
    first_currency_borrowable_amount=SAMPLE_AMOUNT,
    first_currency_credit=SAMPLE_CURRENCY_CREDIT_MODEL,
    id=SAMPLE_ID,
    margin_active=True,
    max_leverage=Decimal("10.0"),
    pair=SAMPLE_PAIR_MODEL,
    second_currency_borrowable_amount=Decimal("1000.00"),
    second_currency_credit=SAMPLE_CURRENCY_CREDIT_MODEL,
    trader=SAMPLE_ID,
    transfer_active=True,
    trigger_price=SAMPLE_TRIGGER_PRICE_MODEL,
)
"""Sample response for get isolated symbol details"""
GET_SYMBOL_DETAILS_SAMPLE_RESPONSE_2: IsolatedSymbolDetailsModel = IsolatedSymbolDetailsModel(
    active=True,
    borrow_active=True,
    break_even_point=SAMPLE_BREAK_EVEN_PRICE_2,
    first_currency_borrowable_amount=SAMPLE_AMOUNT,
    first_currency_credit=SAMPLE_CURRENCY_CREDIT_MODEL_2,
    id=SAMPLE_ID_2,
    margin_active=True,
    max_leverage=Decimal("5.0"),
    pair=SAMPLE_PAIR_MODEL_2,
    second_currency_borrowable_amount=Decimal("500.00"),
    second_currency_credit=SAMPLE_CURRENCY_CREDIT_MODEL_2,
    trader=SAMPLE_ID_2,
    transfer_active=True,
    trigger_price=SAMPLE_TRIGGER_PRICE_MODEL,
)
"""Sample response for get isolated symbol details"""
GET_SYMBOL_DETAILS_SAMPLE_RESPONSE_3: IsolatedSymbolDetailsModel = IsolatedSymbolDetailsModel(
    active=False,
    borrow_active=True,
    break_even_point=SAMPLE_BREAK_EVEN_PRICE_3,
    first_currency_borrowable_amount=SAMPLE_AMOUNT,
    first_currency_credit=SAMPLE_CURRENCY_CREDIT_MODEL_3,
    id=SAMPLE_ID_3,
    margin_active=True,
    max_leverage=Decimal("5.0"),
    pair=SAMPLE_PAIR_MODEL_3,
    second_currency_borrowable_amount=Decimal("500.00"),
    second_currency_credit=SAMPLE_CURRENCY_CREDIT_MODEL_3,
    trader=SAMPLE_ID_3,
    transfer_active=True,
    trigger_price=SAMPLE_TRIGGER_PRICE_MODEL,
)
"""Sample response for get isolated symbol details"""


# Get all margin open orders section
SAMPLE_MARGIN_ORDER_MODEL: MarginOpenOrderModel = MarginOpenOrderModel(
    break_even_point=SAMPLE_BREAK_EVEN_PRICE,
    first_currency_credit=SAMPLE_CURRENCY_CREDIT_MODEL,
    id=SAMPLE_ID,
    isLong=True,
    isOrderFilled=True,
    pair=SAMPLE_PAIR_MODEL,
    risk_name=SAMPLE_RISK_NAME,
    second_currency_credit=SAMPLE_CURRENCY_CREDIT_MODEL,
    trigger_price=SAMPLE_TRIGGER_PRICE_MODEL,
)
"""Sample margin open order model"""
SAMPLE_MARGIN_ORDER_MODEL_2: MarginOpenOrderModel = MarginOpenOrderModel(
    break_even_point=SAMPLE_BREAK_EVEN_PRICE_2,
    first_currency_credit=SAMPLE_CURRENCY_CREDIT_MODEL_2,
    id=SAMPLE_ID_2,
    isLong=False,
    isOrderFilled=False,
    pair=SAMPLE_PAIR_MODEL_2,
    risk_name=SAMPLE_RISK_NAME,
    second_currency_credit=SAMPLE_CURRENCY_CREDIT_MODEL_2,
    trigger_price=SAMPLE_TRIGGER_PRICE_MODEL,
)
"""Sample margin open order model"""
GET_ALL_MARGIN_OPEN_ORDERS_SAMPLE_RESPONSE: list[MarginOpenOrderModel] = [
    SAMPLE_MARGIN_ORDER_MODEL,
    SAMPLE_MARGIN_ORDER_MODEL_2,
]
"""Sample response for get all margin open orders"""
GET_ALL_MARGIN_OPEN_ORDERS_SAMPLE_RESPONSE_SIZE: int = len(
    GET_ALL_MARGIN_OPEN_ORDERS_SAMPLE_RESPONSE,
)
"""Size of sample response for get all margin open orders"""

# OLD DATA
TEST_URI_SUCCESS_CONTENT: str = '{"RESULT": "SUCCESS"}'
"""Success message for get method"""
EXPECTED_CORRECT_GET_RESPONSE_TEXT: dict[str, str] = {"RESULT": "SUCCESS"}
"""Expected response from get uri path"""
TEST_POST_CONTENT: str = "TEST_CONTENT"
"""Sample POST data content"""
TEST_ISOLATED_SYMBOL: str = "TESTUSDT"
"""Test isolated symbol"""
TEST_TABDEAL_SYMBOL: str = "TEST_USDT"
"""Test tabdeal symbol"""
TEST_ISOLATED_SYMBOL_NAME: str = "TEST_SYMBOL_NAME"
"""Test isolated symbol name"""
TEST_MARGIN_ASSET_BALANCE: Decimal = Decimal("470.2352303")
"""Test asset balance"""
TEST_VOLUME_PRECISION: int = 3
"""Test asset volume ordering precision requirements"""
TEST_PRICE_PRECISION: int = 6
"""Test asset price ordering precision requirements"""
UN_TRADE_ABLE_SYMBOL: str = "UN_TRADE_ABLE_SYMBOL"
"""Test Un-trade-able symbol"""
UN_TRADE_ABLE_SYMBOL_DETAILS: str = (
    '{"first_currency_credit":{"currency":{"name":"UN_TRADE_ABLE_SYMBOL_NAME"},'
    '"pair":{"first_currency_precision":14,"price_precision":9}},'
    '"second_currency_credit":{"available_amount":"97.3"},'
    '"id": 99, "pair": {"id": 800},'
    '"borrow_active": true, "transfer_active": false, "active": true}'
)
"""Test un-trade-able symbol"""
INVALID_ISOLATED_SYMBOL: str = "INVALIDUSDT"
"""Invalid isolated symbol"""
INVALID_TYPE_ISOLATED_SYMBOL: str = "INVALID_TYPE_ISOLATED_SYMBOL"
"""Invalid isolated symbol used for testing invalid type response from server"""
NOT_AVAILABLE_FOR_MARGIN_SYMBOL: str = "NOT_AVAILABLE_FOR_MARGIN_TRADING"
"""Isolated symbol that is not available for margin trading"""
TEST_MARGIN_ASSET_ID: int = 123456789
"""Test margin asset ID"""
TEST_ISOLATED_MARGIN_MARKET_GENRE: str = "IsolatedMargin"
"""Test market genre for isolated margin"""
TEST_GET_ALL_MARGIN_OPEN_ORDERS_CONTENT: str = '[{"id": 1, "break_even_point": "5578"}, {"id": 254, "break_even_point": "0.740", "isOrderFilled": false}, {"id": 123456789, "isOrderFilled": true}]'
"""Success message for get all margin open orders method"""
GET_ALL_MARGIN_OPEN_ORDERS_TEST_RESPONSE_ITEM_COUNT: int = 3
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
"""Invalid asset ID to test error handling"""
INVALID_LIST_RESPONSE: str = "[1, 2, 3, 4, 5]"
"""Invalid list response from server to test type error raising"""
INVALID_DICTIONARY_RESPONSE: str = '{"RESULT": "INVALID"}'
"""Invalid dictionary response from server to test type error raising"""
# endregion INVALID RESPONSES

# region HEADERS
INVALID_TYPE_TEST_HEADER: str = "INVALID_TYPE_TEST_HEADER"
"""Test header to test invalid type response from server"""
RAISE_EXCEPTION_TEST_HEADER: str = "RAISE_EXCEPTION_TEST_HEADER"
"""Test header to test exception raising from server"""
# endregion HEADERS

# region MARGIN
# BUY
TEST_BUY_ORDER_PRICE: Decimal = Decimal("0.250")
"""Test order price"""
TEST_BUY_MARGIN_LEVEL: Decimal = Decimal("5.0")
"""Test margin level"""
TEST_BUY_DEPOSIT_AMOUNT: Decimal = Decimal("40.000")
"""Test deposit amount"""
TEST_BUY_ORDER_OBJECT: MarginOrderModel = MarginOrderModel(
    isolated_symbol=SAMPLE_SYMBOL_NAME,
    order_price=TEST_BUY_ORDER_PRICE,
    order_side=OrderSide.BUY,
    margin_level=TEST_BUY_MARGIN_LEVEL,
    deposit_amount=TEST_BUY_DEPOSIT_AMOUNT,
    stop_loss_percent=Decimal(5),
    take_profit_percent=Decimal(5),
    volume_fraction_allowed=True,
    volume_precision=TEST_VOLUME_PRECISION,
)
"""Test order object"""
CORRECT_OPEN_MARGIN_BUY_ORDER_DATA: str = '{"market_id": 170, "side_id": "1", "order_type_id": 1, "amount": "800.000", "borrow_amount": "160.00000000", "market_type": 3, "price": "0.250"}'
"""Correct open margin order data"""
OPEN_MARGIN_BUY_ORDER_SERVER_RESPONSE: str = (
    '{"message": "سفارش با موفقیت ثبت شد.","order": {"id": 6368708172, "state": 4}}'
)
"""Server response for open margin order"""
TEST_BUY_ORDER_ID: int = 6368708172
"""Test order ID"""
SAMPLE_BUY_TOTAL_USDT_AMOUNT: str = "200.00000000"
"""Sample total USDT amount"""
SAMPLE_BUY_BORROWED_USDT_AMOUNT: str = "160.00000000"
"""Sample borrowed USDT amount"""
SAMPLE_BUY_ORDER_VOLUME: str = "800.000"
"""Sample order volume"""
SAMPLE_BUY_BORROWED_VOLUME: str = "640.000"
"""Sample borrowed volume"""
# SELL
GET_SELL_SYMBOL_DETAILS_RESPONSE_CONTENT: str = (
    '{"first_currency_credit":{"currency":{"name":"SELL_SYMBOL_NAME"},'
    '"pair":{"first_currency_precision":0,"price_precision":6}},'
    '"second_currency_credit":{"available_amount":"92.23"},'
    '"id": 90902323, "pair": {"id": 1002},'
    '"borrow_active": true, "transfer_active": true, "active": true}'
)
SAMPLE_SELL_ISOLATED_SYMBOL: str = "SELLUSDT"
"""Sample isolated symbol for sell order"""
TEST_SELL_ORDER_PRICE: Decimal = Decimal("2.9367")
"""Test order price"""
TEST_SELL_MARGIN_LEVEL: Decimal = Decimal("6.5")
"""Test margin level"""
TEST_SELL_DEPOSIT_AMOUNT: Decimal = Decimal(75)
"""Test deposit amount"""
TEST_SELL_ORDER_OBJECT: MarginOrderModel = MarginOrderModel(
    isolated_symbol=SAMPLE_SYMBOL_NAME_2,
    order_price=TEST_SELL_ORDER_PRICE,
    order_side=OrderSide.SELL,
    margin_level=TEST_SELL_MARGIN_LEVEL,
    deposit_amount=TEST_SELL_DEPOSIT_AMOUNT,
    stop_loss_percent=Decimal(10),
    take_profit_percent=Decimal(10),
    volume_fraction_allowed=False,
)
"""Test order object"""
CORRECT_OPEN_MARGIN_SELL_ORDER_DATA: str = '{"market_id": 96503, "side_id": "2", "order_type_id": 1, "amount": "140", "borrow_amount": "140", "market_type": 3, "price": "2.9367"}'
"""Correct open margin order data"""
OPEN_MARGIN_SELL_ORDER_SERVER_RESPONSE: str = (
    '{"message": "سفارش با موفقیت ثبت شد.","order": {"id": 9092301030, "state": 1}}'
)
"""Server response for open margin order"""
TEST_SELL_ORDER_ID: int = 9092301030
"""Test sell order ID"""
SAMPLE_SELL_TOTAL_USDT_AMOUNT: str = "412.50000000"
"""Sample total USDT amount"""
SAMPLE_SELL_BORROWED_USDT_AMOUNT: str = "337.50000000"
"""Sample borrowed USDT amount"""
SAMPLE_SELL_ORDER_VOLUME: str = "140"
"""Sample order volume"""
SAMPLE_SELL_BORROWED_VOLUME: str = "114"
"""Sample borrowed volume"""
SAMPLE_MARGIN_ASSET_ID: int = 5004002
"""Sample margin asset ID"""

# endregion MARGIN

# region order
SAMPLE_GET_ORDERS_HISTORY_RESPONSE: str = (
    '{"orders":['
    '{"created": "2024-11-09T14:06:32.264779+03:30","id": 5938280017,"side": 1,'
    '"state": 2,"amount": 990.0,"price": 0.001197,"filled_amount": 970.0,'
    '"average_price": 0.001157},'
    '{"created": "2024-10-11T08:07:32.264779+03:30","id": 3288090001,"side": 2,'
    '"state": 4,"amount": 10200.0,"price": 0.001084,"filled_amount": 10200.0,'
    '"average_price": 0.001083},'
    '{"created": "2024-09-12T14:06:32.264779+03:30","id": 4038289911,"side": 1,'
    '"state": 4,"amount": 970.0,"price": 0.001197,"filled_amount": 970.0,'
    '"average_price": 0.001157}]}'
)
"""Sample response from server on getting orders history"""
SAMPLE_GET_ORDERS_HISTORY_LIST: list[dict[str, Any]] = [
    {
        "created": "2024-11-09T14:06:32.264779+03:30",
        "id": 5938280017,
        "side": 1,
        "state": 2,
        "amount": 990.0,
        "price": 0.001197,
        "filled_amount": 970.0,
        "average_price": 0.001157,
    },
    {
        "created": "2024-10-11T08:07:32.264779+03:30",
        "id": 3288090001,
        "side": 2,
        "state": 4,
        "amount": 10200.0,
        "price": 0.001084,
        "filled_amount": 10200.0,
        "average_price": 0.001083,
    },
    {
        "created": "2024-09-12T14:06:32.264779+03:30",
        "id": 4038289911,
        "side": 1,
        "state": 4,
        "amount": 970.0,
        "price": 0.001197,
        "filled_amount": 970.0,
        "average_price": 0.001157,
    },
]
"""Sample processed response from server on getting orders history"""
SAMPLE_MAX_HISTORY: int = 323
"""Sample max history query to verify query request"""
SAMPLE_ORDERS_LIST_ITEMS_COUNT: int = 3
"""Number of items in the sample list to verify the list"""
SAMPLE_ORDER_ID: int = 4038289911
"""Sample order ID in the sample data"""
SAMPLE_INVALID_ORDER_ID: int = 9999999999999999
"""Sample invalid order ID"""
SAMPLE_MARGIN_LEVEL: Decimal = Decimal("6.3")
"""Sample margin level"""
# endregion order

# region UTILITIES
FIRST_SAMPLE_ORDER_PRICE: Decimal = Decimal("42.197")
"""Sample order price"""
# endregion UTILITIES

# region Wallet tests
SAMPLE_GET_WALLET_USDT_DETAILS_RESPONSE: str = '{"TetherUS":79.231904,"Toman":10.0}'
"""Sample response from server when requesting wallet USDT details"""
SAMPLE_WALLET_USDT_BALANCE: Decimal = Decimal("79.231904")
"""Sample wallet USDT balance"""
TEST_USDT_MARKET_ID: str = "3"
"""USDT Market ID"""
SAMPLE_TRANSFER_USDT: Decimal = Decimal("44.50")
"""Sample transfer USDT to margin asset amount"""
SUCCESSFUL_TRANSFER_USDT_TO_MARGIN_ASSET_RESPONSE: str = '{"message": "انتقال با موفقیت انجام شد."}'
"""Response from server when transferring USDT to margin asset is successful"""
SUCCESSFUL_TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_RESPONSE: str = (
    '{"created": "2020-11-20T19:50:13.024598Z"}'
)
"""Response from server when transferring USDT from margin asset to wallet is successful"""
# endregion Wallet tests

# region MISC
TEST_TRUE: str = "true"
"""String representation of True"""
# endregion MISC
