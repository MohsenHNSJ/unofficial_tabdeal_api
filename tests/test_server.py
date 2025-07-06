"""This file is for holding test server functions."""
# ruff: noqa: E501, PLR0911
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable"
# pylint: disable=W0613,W0612,C0301

import json
from decimal import Decimal
from typing import Any

from aiohttp import web

from tests.test_constants import (
    CORRECT_OPEN_MARGIN_BUY_ORDER_DATA,
    CORRECT_OPEN_MARGIN_SELL_ORDER_DATA,
    GET_ALL_MARGIN_OPEN_ORDERS_SAMPLE_RESPONSE,
    GET_SELL_SYMBOL_DETAILS_RESPONSE_CONTENT,
    GET_SYMBOL_DETAILS_SAMPLE_RESPONSE,
    GET_SYMBOL_DETAILS_SAMPLE_RESPONSE_2,
    GET_SYMBOL_DETAILS_SAMPLE_RESPONSE_3,
    INVALID_DICTIONARY_RESPONSE,
    INVALID_LIST_RESPONSE,
    INVALID_TYPE_ISOLATED_SYMBOL,
    INVALID_TYPE_TEST_HEADER,
    NOT_AVAILABLE_FOR_MARGIN_SYMBOL,
    OPEN_MARGIN_BUY_ORDER_SERVER_RESPONSE,
    OPEN_MARGIN_SELL_ORDER_SERVER_RESPONSE,
    RAISE_EXCEPTION_TEST_HEADER,
    SAMPLE_GENRE,
    SAMPLE_GET_ORDERS_HISTORY_RESPONSE,
    SAMPLE_GET_WALLET_USDT_DETAILS_RESPONSE,
    SAMPLE_MARGIN_ASSET_ID,
    SAMPLE_MAX_HISTORY,
    SAMPLE_SELL_ISOLATED_SYMBOL,
    SAMPLE_STOP_LOSS_PRICE,
    SAMPLE_SYMBOL_NAME,
    SAMPLE_SYMBOL_NAME_2,
    SAMPLE_SYMBOL_NAME_3,
    SAMPLE_TAKE_PROFIT_PRICE,
    SAMPLE_WALLET_USDT_BALANCE,
    STATUS_IM_A_TEAPOT,
    SUCCESSFUL_TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_RESPONSE,
    SUCCESSFUL_TRANSFER_USDT_TO_MARGIN_ASSET_RESPONSE,
    TEST_ISOLATED_MARGIN_MARKET_GENRE,
    TEST_ISOLATED_SYMBOL,
    TEST_POST_CONTENT,
    TEST_TABDEAL_SYMBOL,
    TEST_TRUE,
    TEST_URI_PATH,
    TEST_URI_SUCCESS_CONTENT,
    TEST_USDT_MARKET_ID,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
    UNKNOWN_URI_PATH,
    USER_UNAUTHORIZED_RESPONSE,
)
from unofficial_tabdeal_api.constants import (
    GENERIC_SERVER_CONFIRMATION_RESPONSE,
    GET_ALL_MARGIN_OPEN_ORDERS_URI,
    GET_MARGIN_ASSET_DETAILS_URI,
    GET_ORDERS_HISTORY_URI,
    GET_WALLET_USDT_BALANCE_URI,
    MARGIN_NOT_ACTIVE_RESPONSE,
    MARGIN_POSITION_NOT_FOUND_RESPONSE,
    MARKET_NOT_FOUND_RESPONSE,
    OPEN_MARGIN_ORDER_URI,
    ORDER_IS_INVALID_RESPONSE,
    REQUESTED_PARAMETERS_INVALID_RESPONSE,
    SET_SL_TP_FOR_MARGIN_ORDER_URI,
    STATUS_BAD_REQUEST,
    STATUS_UNAUTHORIZED,
    TRANSFER_AMOUNT_OVER_ACCOUNT_BALANCE_RESPONSE,
    TRANSFER_FROM_MARGIN_ASSET_TO_WALLET_NOT_POSSIBLE_RESPONSE,
    TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_URI,
    TRANSFER_USDT_TO_MARGIN_ASSET_URI,
)


async def server_get_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server."""
    # Check if request header is correct
    user_hash: str | None = request.headers.get("user-hash")
    user_auth_key: str | None = request.headers.get("Authorization")
    if (user_hash != TEST_USER_HASH) or (user_auth_key != TEST_USER_AUTH_KEY):
        # Return 401 UnAuthorized in case of authorization failure
        return web.Response(
            status=STATUS_UNAUTHORIZED,
            text=USER_UNAUTHORIZED_RESPONSE,
        )

    # Check request path and execute corresponding function
    result: web.Response
    match request.path:
        # GET: Isolated symbol details
        case _ if request.path == GET_MARGIN_ASSET_DETAILS_URI:
            result = symbol_details_query_responder(request=request)

        # GET: Margin all open orders
        case _ if request.path == GET_ALL_MARGIN_OPEN_ORDERS_URI:
            result = all_margin_open_orders_responder(request=request)

        # GET: Wallet USDT balance
        case _ if request.path == GET_WALLET_USDT_BALANCE_URI:
            result = wallet_details_query_responder(request=request)

        # GET: Orders details history
        case _ if request.path == GET_ORDERS_HISTORY_URI:
            result = orders_history_responder(request=request)

        # GET: Unknown request path
        case _ if request.path == UNKNOWN_URI_PATH:
            result = server_unknown_error_responder(request=request)

        # Default case, Simple auth test
        case _:
            result = web.Response(
                text=TEST_URI_SUCCESS_CONTENT,
            )

    return result


async def server_post_responder(request: web.Request) -> web.Response:
    """Mocks the POST response from server."""
    # Check if the request header is correct
    user_hash: str | None = request.headers.get("user-hash")
    user_auth_key: str | None = request.headers.get("Authorization")
    if (user_hash != TEST_USER_HASH) or (user_auth_key != TEST_USER_AUTH_KEY):
        return web.Response(
            status=STATUS_UNAUTHORIZED,
            text=USER_UNAUTHORIZED_RESPONSE,
        )

    # Check request path and execute corresponding function
    result: web.Response
    match request.path:
        # POST: Margin order
        case _ if request.path == OPEN_MARGIN_ORDER_URI:
            result = await open_margin_order_responder(request=request)

        # POST: Test function
        case _ if request.path == TEST_URI_PATH:  # pragma: no cover
            result = await post_test_content_responder(request=request)

        # POST: Transfer USDT from wallet to margin asset
        case _ if request.path == TRANSFER_USDT_TO_MARGIN_ASSET_URI:
            result = await transfer_usdt_from_wallet_to_margin_asset_responder(request=request)

        # POST: Transfer USDT from margin asset to wallet
        case _ if request.path == TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_URI:
            result = await transfer_usdt_from_margin_asset_to_wallet_responder(request=request)

        # POST: Set SL/TP for margin order
        case _ if request.path == SET_SL_TP_FOR_MARGIN_ORDER_URI:
            result = await set_sl_tp_for_margin_order_responder(request=request)

        # Default case, Unknown
        case _:  # pragma: no cover
            result = web.Response(
                status=STATUS_BAD_REQUEST,
                text="Unknown request",
            )

    return result


def server_unknown_error_responder(request: web.Request) -> web.Response:
    """Returns an unknown error code from server (418 for example)."""
    return web.Response(
        status=STATUS_IM_A_TEAPOT,
        text=f"The requested entity body is short and stout.\nTip me over and pour me out.\nRequest Type: [{request.method}]",
    )


def symbol_details_query_responder(request: web.Request) -> web.Response:
    """Responds to queries for symbol details.

    Args:
        request (web.Request): Request object

    Returns:
        web.Response: Request response
    """
    # Extract query parameters
    pair_symbol: str | None = request.query.get("pair_symbol")
    account_genre: str | None = request.query.get("account_genre")

    # If query is correct, return symbol details
    if (pair_symbol == SAMPLE_SYMBOL_NAME) and (account_genre == SAMPLE_GENRE):
        # Return symbol details
        return web.Response(text=GET_SYMBOL_DETAILS_SAMPLE_RESPONSE.model_dump_json())

    # If query is for second test symbol, return data
    if (pair_symbol == SAMPLE_SYMBOL_NAME_2) and (account_genre == SAMPLE_GENRE):
        return web.Response(text=GET_SYMBOL_DETAILS_SAMPLE_RESPONSE_2.model_dump_json())

    # If query is for un-trade-able symbol, return un-trade-able symbol details
    if (pair_symbol == SAMPLE_SYMBOL_NAME_3) and (account_genre == SAMPLE_GENRE):
        # Return symbol details
        return web.Response(text=GET_SYMBOL_DETAILS_SAMPLE_RESPONSE_3.model_dump_json())

    # If query is not available for margin trading symbol, return 400 and response
    if (pair_symbol == NOT_AVAILABLE_FOR_MARGIN_SYMBOL) and (
        account_genre == TEST_ISOLATED_MARGIN_MARKET_GENRE
    ):
        return web.Response(text=MARGIN_NOT_ACTIVE_RESPONSE, status=STATUS_BAD_REQUEST)

    # If query is a test for invalid type returning
    if (pair_symbol == INVALID_TYPE_ISOLATED_SYMBOL) and (
        account_genre == TEST_ISOLATED_MARGIN_MARKET_GENRE
    ):
        return web.Response(text=INVALID_LIST_RESPONSE)

    if (
        pair_symbol == SAMPLE_SELL_ISOLATED_SYMBOL
        and account_genre == TEST_ISOLATED_MARGIN_MARKET_GENRE
    ):
        # Return symbol details
        return web.Response(text=GET_SELL_SYMBOL_DETAILS_RESPONSE_CONTENT)

    # Else, the query is invalid, return 400 Bad Request
    return web.Response(text=MARKET_NOT_FOUND_RESPONSE, status=STATUS_BAD_REQUEST)


def wallet_details_query_responder(request: web.Request) -> web.Response:
    """Responds to queries for wallet details."""
    # Extract request query and headers
    market_id: str | None = request.query.get("market_id")
    is_raise_exception_test: bool = (
        request.headers.get(
            RAISE_EXCEPTION_TEST_HEADER,
        )
        is not None
    )
    is_invalid_response_type_test: bool = (
        request.headers.get(
            INVALID_TYPE_TEST_HEADER,
        )
        is not None
    )

    # If testing for invalid data type response
    if is_invalid_response_type_test:
        # Return invalid type response
        return web.Response(
            text=INVALID_LIST_RESPONSE,
        )

    # If query is for USDT balance, return USDT Balance
    if market_id == TEST_USDT_MARKET_ID and not is_raise_exception_test:
        return web.Response(text=SAMPLE_GET_WALLET_USDT_DETAILS_RESPONSE)

    # Else, the query is invalid, return 400 Bad Request
    return web.Response(text=MARKET_NOT_FOUND_RESPONSE, status=STATUS_BAD_REQUEST)


def orders_history_responder(request: web.Request) -> web.Response:
    """Responds to queries for orders history."""
    # Extract queries and headers
    page_size: str | None = request.query.get("page_size")  # Max history
    ordering: str | None = request.query.get("ordering")
    descending: str | None = request.query.get("desc")
    market_type: str | None = request.query.get("market_type")
    order_type: str | None = request.query.get("order_type")
    is_invalid_response_type_test: bool = (
        request.headers.get(
            INVALID_TYPE_TEST_HEADER,
        )
        is not None
    )
    # If testing for invalid type response
    if is_invalid_response_type_test:
        # Return invalid type response
        return web.Response(
            text=INVALID_LIST_RESPONSE,
        )

    # If query is correct, return the sample response
    if (
        (page_size == str(object=SAMPLE_MAX_HISTORY) or page_size == str(500))
        and ordering == "created"
        and descending == "true"
        and market_type == "All"
        and order_type == "All"
    ):
        return web.Response(text=SAMPLE_GET_ORDERS_HISTORY_RESPONSE)

    # Else, the query is invalid, return 400 Bad Request
    return web.Response(text=REQUESTED_PARAMETERS_INVALID_RESPONSE, status=STATUS_BAD_REQUEST)


def all_margin_open_orders_responder(request: web.Request) -> web.Response:
    """Responds to queries for all margin open orders."""
    # If the request is for testing invalid server response type:
    if request.headers.get(INVALID_TYPE_TEST_HEADER) == TEST_TRUE:
        # Return invalid type response
        return web.Response(
            text=INVALID_DICTIONARY_RESPONSE,
        )
    # Create the response from sample data
    json_text: str = json.dumps(
        obj=[item.model_dump() for item in GET_ALL_MARGIN_OPEN_ORDERS_SAMPLE_RESPONSE],
        ensure_ascii=False,  # Preserver persian texts
        default=str,  # Handles Decimals and other non-serializable types
    )
    return web.Response(text=json_text)


async def open_margin_order_responder(request: web.Request) -> web.Response:
    """Responds to requests to open margin orders."""
    # Extract request data and headers
    data: str = await request.text()
    is_invalid_type_test: bool = (
        request.headers.get(
            INVALID_TYPE_TEST_HEADER,
        )
        is not None
    )
    # If request has invalid type test header, respond invalid type (list)
    if is_invalid_type_test:
        return web.Response(
            text=f"[{OPEN_MARGIN_BUY_ORDER_SERVER_RESPONSE}, {OPEN_MARGIN_SELL_ORDER_SERVER_RESPONSE}]",
        )

    # If the request is BUY, respond valid
    if data == CORRECT_OPEN_MARGIN_BUY_ORDER_DATA:
        return web.Response(text=OPEN_MARGIN_BUY_ORDER_SERVER_RESPONSE)

    # If the request is SELL, respond valid
    if data == CORRECT_OPEN_MARGIN_SELL_ORDER_DATA:  # pragma: no cover
        return web.Response(text=OPEN_MARGIN_SELL_ORDER_SERVER_RESPONSE)

    # Else, return invalid
    return web.Response(
        status=STATUS_BAD_REQUEST,
        text=ORDER_IS_INVALID_RESPONSE,
    )  # pragma: no cover


async def post_test_content_responder(request: web.Request) -> web.Response:
    """Responds to requests for test post content."""
    # Extract request data
    data: str = await request.text()
    # If the request is processed correctly, respond valid
    if data == TEST_POST_CONTENT:
        return web.Response(text=TEST_URI_SUCCESS_CONTENT)

    # Else, return invalid
    return web.Response(status=STATUS_BAD_REQUEST, text=REQUESTED_PARAMETERS_INVALID_RESPONSE)


async def transfer_usdt_from_wallet_to_margin_asset_responder(request: web.Request) -> web.Response:
    """Responds to requests for transferring USDT from wallet to margin asset."""
    # Extract request data
    data: dict[str, Any] = json.loads(s=await request.text())
    constant_amount: Decimal = Decimal(value=data["amount"])
    currency_symbol: str = data["currency_symbol"]
    transfer_amount: Decimal = Decimal(data["transfer_amount_from_main"])
    pair_symbol: str = data["pair_symbol"]

    # Check constant amount to be 0
    if constant_amount != 0:  # pragma: no cover
        return web.Response(  # pragma: no cover
            status=STATUS_BAD_REQUEST,
            text=REQUESTED_PARAMETERS_INVALID_RESPONSE,
        )

    # Check currency symbol to be USDT
    if currency_symbol != "USDT":  # pragma: no cover
        return web.Response(  # pragma: no cover
            status=STATUS_BAD_REQUEST,
            text=REQUESTED_PARAMETERS_INVALID_RESPONSE,
        )

    # Check pair symbol to be TEST_USDT
    if pair_symbol != TEST_TABDEAL_SYMBOL:  # pragma: no cover
        return web.Response(  # pragma: no cover
            status=STATUS_BAD_REQUEST,
            text=REQUESTED_PARAMETERS_INVALID_RESPONSE,
        )

    # If the requested amount is lower than account balance, respond successfully
    if transfer_amount <= SAMPLE_WALLET_USDT_BALANCE:
        return web.Response(text=SUCCESSFUL_TRANSFER_USDT_TO_MARGIN_ASSET_RESPONSE)

    # If the requested amount is higher than account balance, respond invalid
    if transfer_amount > SAMPLE_WALLET_USDT_BALANCE:
        return web.Response(
            status=STATUS_BAD_REQUEST,
            text=TRANSFER_AMOUNT_OVER_ACCOUNT_BALANCE_RESPONSE,
        )

    # Else, return invalid
    return web.Response(
        status=STATUS_BAD_REQUEST,
        text=REQUESTED_PARAMETERS_INVALID_RESPONSE,
    )  # pragma: no cover


async def transfer_usdt_from_margin_asset_to_wallet_responder(request: web.Request) -> web.Response:
    """Responds to requests for transferring USDT from wallet to margin asset."""
    # Extract request data
    data: dict[str, Any] = json.loads(s=await request.text())
    transfer_direction: str = data["transfer_direction"]
    transfer_amount: Decimal = Decimal(value=data["amount"])
    currency_symbol: str = data["currency_symbol"]
    account_genre: str = data["account_genre"]
    other_account_genre: str = data["other_account_genre"]
    pair_symbol: str = data["pair_symbol"]

    # Check transfer direction set to "Out"
    if (transfer_direction != "Out") or (other_account_genre != "Main"):  # pragma: no cover
        return web.Response(  # pragma: no cover
            status=STATUS_BAD_REQUEST,
            text=REQUESTED_PARAMETERS_INVALID_RESPONSE,
        )

    # Check currency symbol to be "USDT" and account genre set to "IsolatedMargin"
    if (currency_symbol != "USDT") or (account_genre != "IsolatedMargin"):  # pragma: no cover
        return web.Response(  # pragma: no cover
            status=STATUS_BAD_REQUEST,
            text=REQUESTED_PARAMETERS_INVALID_RESPONSE,
        )

    # Check pair symbol to be TEST_USDT
    if pair_symbol != TEST_ISOLATED_SYMBOL:  # pragma: no cover
        return web.Response(  # pragma: no cover
            status=STATUS_BAD_REQUEST,
            text=REQUESTED_PARAMETERS_INVALID_RESPONSE,
        )

    # If the requested amount is lower than account balance, respond successfully
    if transfer_amount <= SAMPLE_WALLET_USDT_BALANCE:
        return web.Response(text=SUCCESSFUL_TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_RESPONSE)

    # If the requested amount is higher than account balance, respond invalid
    if transfer_amount > SAMPLE_WALLET_USDT_BALANCE:
        return web.Response(
            status=STATUS_BAD_REQUEST,
            text=TRANSFER_FROM_MARGIN_ASSET_TO_WALLET_NOT_POSSIBLE_RESPONSE,
        )

    # Else, return invalid
    return web.Response(
        status=STATUS_BAD_REQUEST,
        text=REQUESTED_PARAMETERS_INVALID_RESPONSE,
    )  # pragma: no cover


async def set_sl_tp_for_margin_order_responder(request: web.Request) -> web.Response:
    """Responds to requests for setting SL and TP points for margin order."""
    # Extract request data
    data: dict[str, Any] = json.loads(s=await request.text())
    margin_asset_id: int = data["trader_isolated_margin_id"]
    stop_loss_price: Decimal = Decimal(value=data["sl_price"])
    take_profit_price: Decimal = Decimal(value=data["tp_price"])

    # Check parameters
    if (
        (margin_asset_id != SAMPLE_MARGIN_ASSET_ID)
        or (stop_loss_price != SAMPLE_STOP_LOSS_PRICE)
        or (take_profit_price != SAMPLE_TAKE_PROFIT_PRICE)
    ):
        return web.Response(status=STATUS_BAD_REQUEST, text=MARGIN_POSITION_NOT_FOUND_RESPONSE)

    # Server responds a generic '"درخواست مورد نظر با موفقیت انجام شد."' message
    # Even if i try to set SL/TP for an asset that does not have an active margin order
    # The server only complains when the margin asset ID is not correct
    # So, we also send a generic CODE 200 with empty message
    return web.Response(text=GENERIC_SERVER_CONFIRMATION_RESPONSE)
