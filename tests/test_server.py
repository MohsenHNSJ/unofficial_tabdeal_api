"""This file is for holding test server functions."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable"
# pylint: disable=W0613,W0612,C0301

from aiohttp import web

from tests.test_constants import (
    GET_SYMBOL_DETAILS_RESPONSE_CONTENT,
    INVALID_DICTIONARY_RESPONSE,
    INVALID_LIST_RESPONSE,
    INVALID_TYPE_ISOLATED_SYMBOL,
    INVALID_TYPE_TEST_HEADER,
    NOT_AVAILABLE_FOR_MARGIN_SYMBOL,
    RAISE_EXCEPTION_TEST_HEADER,
    SAMPLE_GET_ORDERS_HISTORY_RESPONSE,
    SAMPLE_GET_WALLET_USDT_DETAILS_RESPONSE,
    SAMPLE_MAX_HISTORY,
    STATUS_IM_A_TEAPOT,
    TEST_GET_ALL_MARGIN_OPEN_ORDERS_CONTENT,
    TEST_ISOLATED_MARGIN_MARKET_GENRE,
    TEST_ISOLATED_SYMBOL,
    TEST_POST_CONTENT,
    TEST_TRUE,
    TEST_URI_SUCCESS_CONTENT,
    TEST_USDT_MARKET_ID,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
    UN_TRADE_ABLE_SYMBOL,
    UN_TRADE_ABLE_SYMBOL_DETAILS,
)
from unofficial_tabdeal_api.constants import (
    GET_ALL_MARGIN_OPEN_ORDERS_URI,
    GET_MARGIN_ASSET_DETAILS_URI,
    GET_ORDERS_HISTORY_URI,
    GET_WALLET_USDT_BALANCE_URI,
    MARGIN_NOT_ACTIVE_RESPONSE,
    MARKET_NOT_FOUND_RESPONSE,
    REQUESTED_PARAMETERS_INVALID,
    STATUS_BAD_REQUEST,
    STATUS_UNAUTHORIZED,
)


# TODO: Refactor into a dispatcher or class-based router for cleaner logic
async def server_get_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server."""
    # Check if request header is correct
    user_hash: str | None = request.headers.get("user-hash")
    user_auth_key: str | None = request.headers.get("Authorization")
    if (user_hash != TEST_USER_HASH) or (user_auth_key != TEST_USER_AUTH_KEY):
        # Return 401 UnAuthorized in case of authorization failure
        return web.Response(
            status=STATUS_UNAUTHORIZED,
            text='{"detail":"Token is invalid or expired"}',
        )

    # Check request path and execute corresponding function
    match request.path:
        # GET: Isolated symbol details
        case _ if request.path == GET_MARGIN_ASSET_DETAILS_URI:
            result = await symbol_details_query_responder(request)
        # GET: Margin all open orders
        case _ if request.path == GET_ALL_MARGIN_OPEN_ORDERS_URI:
            result = await all_margin_open_orders_responder(request)
        # GET: Wallet USDT balance
        case _ if request.path == GET_WALLET_USDT_BALANCE_URI:
            result = await wallet_details_query_responder(request)

        # GET: Orders details history
        case _ if request.path == GET_ORDERS_HISTORY_URI:
            result = await orders_history_responder(request)

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
            text=f"Got invalid authentication headers.\nHash:{user_hash}\nAuth key:{user_auth_key}",
        )
    # Check if the content is correct
    if await request.text() != TEST_POST_CONTENT:
        return web.Response(
            status=STATUS_BAD_REQUEST,
            text=f"Expected:{TEST_POST_CONTENT}\nGot:{await request.text()}",
        )

    # Else, the headers, request type and content is correct
    return web.Response(text=TEST_URI_SUCCESS_CONTENT)


async def server_unknown_error_responder(request: web.Request) -> web.Response:
    """Returns an unknown error code from server (418 for example)."""
    return web.Response(
        status=STATUS_IM_A_TEAPOT,
        text=f"The requested entity body is short and stout.\nTip me over and pour me out.\nRequest Type: [{request.method}]",
    )


async def symbol_details_query_responder(request: web.Request) -> web.Response:
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
    if (pair_symbol == TEST_ISOLATED_SYMBOL) and (
        account_genre == TEST_ISOLATED_MARGIN_MARKET_GENRE
    ):
        # Return symbol details
        return web.Response(text=GET_SYMBOL_DETAILS_RESPONSE_CONTENT)

    # If query is for un-trade-able symbol, return un-trade-able symbol details
    if (pair_symbol == UN_TRADE_ABLE_SYMBOL) and (
        account_genre == TEST_ISOLATED_MARGIN_MARKET_GENRE
    ):
        # Return symbol details
        return web.Response(text=UN_TRADE_ABLE_SYMBOL_DETAILS)

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

    # Else, the query is invalid, return 400 Bad Request
    return web.Response(text=MARKET_NOT_FOUND_RESPONSE, status=STATUS_BAD_REQUEST)


async def wallet_details_query_responder(request: web.Request) -> web.Response:
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


async def orders_history_responder(request: web.Request) -> web.Response:
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
        (page_size == str(SAMPLE_MAX_HISTORY) or page_size == str(500))
        and ordering == "created"
        and descending == "true"
        and market_type == "All"
        and order_type == "All"
    ):
        return web.Response(text=SAMPLE_GET_ORDERS_HISTORY_RESPONSE)

    # Else, the query is invalid, return 400 Bad Request
    return web.Response(text=REQUESTED_PARAMETERS_INVALID, status=STATUS_BAD_REQUEST)


async def all_margin_open_orders_responder(request: web.Request) -> web.Response:
    """Responds to queries for all margin open orders."""
    # If the request is for testing invalid server response type:
    if request.headers.get(INVALID_TYPE_TEST_HEADER) == TEST_TRUE:
        # Return invalid type response
        return web.Response(
            text=INVALID_DICTIONARY_RESPONSE,
        )
    return web.Response(text=TEST_GET_ALL_MARGIN_OPEN_ORDERS_CONTENT)
