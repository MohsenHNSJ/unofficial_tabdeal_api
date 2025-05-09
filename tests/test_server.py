"""This file is for holding test server functions."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable"
# pylint: disable=W0613,W0612,C0301

from aiohttp import web

from tests.test_constants import (
    GET_SYMBOL_DETAILS_RESPONSE_CONTENT,
    NOT_AVAILABLE_FOR_MARGIN_SYMBOL,
    STATUS_IM_A_TEAPOT,
    TEST_GET_ALL_MARGIN_OPEN_ORDERS_CONTENT,
    TEST_ISOLATED_MARGIN_MARKET_GENRE,
    TEST_ISOLATED_SYMBOL,
    TEST_POST_CONTENT,
    TEST_URI_SUCCESS_CONTENT,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
    UN_TRADE_ABLE_SYMBOL,
    UN_TRADE_ABLE_SYMBOL_DETAILS,
)
from unofficial_tabdeal_api.constants import (
    GET_ALL_MARGIN_OPEN_ORDERS_URI,
    MARGIN_NOT_ACTIVE_RESPONSE,
    MARKET_NOT_FOUND_RESPONSE,
    STATUS_BAD_REQUEST,
    STATUS_UNAUTHORIZED,
)


async def server_get_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server."""
    # Check if the request header is correct
    user_hash: str | None = request.headers.get("user-hash")
    user_auth_key: str | None = request.headers.get("Authorization")
    if (user_hash != TEST_USER_HASH) or (user_auth_key != TEST_USER_AUTH_KEY):
        # Return 401 UnAuthorized in case of authorization failure
        return web.Response(
            status=STATUS_UNAUTHORIZED,
            text='{"detail":"Token is invalid or expired"}',
        )

    # Check if the request has a query for symbol details
    pair_symbol: str | None = request.query.get("pair_symbol")
    account_genre: str | None = request.query.get("account_genre")
    # If there is a query, return the parsed data from query_responder
    if (pair_symbol is not None) and (account_genre is not None):
        return await query_responder(pair_symbol, account_genre)

    # Check if request is asking for all open margin orders
    if request.path == GET_ALL_MARGIN_OPEN_ORDERS_URI:
        return web.Response(text=TEST_GET_ALL_MARGIN_OPEN_ORDERS_CONTENT)

    # Else, the headers and request type is correct and it's a simple GET request
    return web.Response(text=TEST_URI_SUCCESS_CONTENT)


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


async def query_responder(pair_symbol: str, account_genre: str) -> web.Response:
    """Responds to queries from test user.

    Args:
        pair_symbol (str): Asset pair symbol
        account_genre (str): Account genre of asset pair

    Returns:
        web.Response: Request response
    """
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

    # Else, the query is invalid, return 400 Bad Request
    return web.Response(text=MARKET_NOT_FOUND_RESPONSE, status=STATUS_BAD_REQUEST)
