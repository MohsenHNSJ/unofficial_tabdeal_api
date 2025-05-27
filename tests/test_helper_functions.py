"""This file contains helper functions used for testing only."""
# ruff: noqa: ANN001
# mypy: disable-error-code="no-untyped-def,type-arg"

from collections.abc import Callable

import aiohttp
from aiohttp import test_utils, web

from tests.test_constants import (
    TEST_SERVER_PORT,
    TEST_URI_PATH,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
    UNKNOWN_URI_PATH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_server import server_get_responder, server_post_responder
from unofficial_tabdeal_api.constants import (
    GET_ACCOUNT_PREFERENCES_URI,
    GET_ALL_MARGIN_OPEN_ORDERS_URI,
    GET_MARGIN_ASSET_DETAILS_URI,
    GET_ORDERS_HISTORY_URI,
    GET_WALLET_USDT_BALANCE_URI,
    OPEN_MARGIN_ORDER_URI,
    SET_SL_TP_FOR_MARGIN_ORDER_URI,
    TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_URI,
    TRANSFER_USDT_TO_MARGIN_ASSET_URI,
)
from unofficial_tabdeal_api.tabdeal_client import TabdealClient


class Endpoint:
    """Endpoint class to hold endpoint data."""

    def __init__(self, *, uri: str, method: HttpRequestMethod, function_handler: Callable) -> None:
        """Initializes the Endpoint object.

        Args:
            uri (str): Endpoint URI
            method (HttpRequestMethod): HTTP request method
            function_handler (Callable): Function to handle the request
        """
        self.uri: str = uri
        self.method: HttpRequestMethod = method
        self.function_handler: Callable = function_handler


# region ENDPOINTS
UNKNOWN_ENDPOINT: Endpoint = Endpoint(
    uri=UNKNOWN_URI_PATH,
    method=HttpRequestMethod.GET,
    function_handler=server_get_responder,
)
"""Endpoint for unknown URI path."""
BASE_TEST_GET_ENDPOINT: Endpoint = Endpoint(
    uri=TEST_URI_PATH,
    method=HttpRequestMethod.GET,
    function_handler=server_get_responder,
)
"""Base endpoint for testing GET."""
BASE_TEST_POST_ENDPOINT: Endpoint = Endpoint(
    uri=TEST_URI_PATH,
    method=HttpRequestMethod.POST,
    function_handler=server_post_responder,
)
"""Base endpoint for testing POST."""
GET_ACCOUNT_PREFERENCES_ENDPOINT: Endpoint = Endpoint(
    uri=GET_ACCOUNT_PREFERENCES_URI,
    method=HttpRequestMethod.GET,
    function_handler=server_get_responder,
)
"""Endpoint for get account preferences"""
GET_MARGIN_ASSET_DETAILS_ENDPOINT: Endpoint = Endpoint(
    uri=GET_MARGIN_ASSET_DETAILS_URI,
    method=HttpRequestMethod.GET,
    function_handler=server_get_responder,
)
"""Endpoint for get margin asset details"""
GET_ALL_MARGIN_OPEN_ORDERS_ENDPOINT: Endpoint = Endpoint(
    uri=GET_ALL_MARGIN_OPEN_ORDERS_URI,
    method=HttpRequestMethod.GET,
    function_handler=server_get_responder,
)
"""Endpoint for get all margin open orders"""
GET_ORDERS_HISTORY_ENDPOINT: Endpoint = Endpoint(
    uri=GET_ORDERS_HISTORY_URI,
    method=HttpRequestMethod.GET,
    function_handler=server_get_responder,
)
"""Endpoint for get orders history"""
OPEN_MARGIN_ORDER_ENDPOINT: Endpoint = Endpoint(
    uri=OPEN_MARGIN_ORDER_URI,
    method=HttpRequestMethod.POST,
    function_handler=server_post_responder,
)
"""Endpoint for open margin order"""
GET_SYMBOL_DETAILS_ENDPOINT: Endpoint = Endpoint(
    uri=GET_MARGIN_ASSET_DETAILS_URI,
    method=HttpRequestMethod.GET,
    function_handler=server_get_responder,
)
"""Endpoint for get margin asset details"""
SET_SL_TP_FOR_MARGIN_ORDER_ENDPOINT: Endpoint = Endpoint(
    uri=SET_SL_TP_FOR_MARGIN_ORDER_URI,
    method=HttpRequestMethod.POST,
    function_handler=server_post_responder,
)
"""Endpoint for setting SL/TP points"""
GET_WALLET_USDT_BALANCE_ENDPOINT: Endpoint = Endpoint(
    uri=GET_WALLET_USDT_BALANCE_URI,
    method=HttpRequestMethod.GET,
    function_handler=server_get_responder,
)
"""Endpoint for get wallet USDT balance"""
TRANSFER_USDT_TO_MARGIN_ASSET_ENDPOINT: Endpoint = Endpoint(
    uri=TRANSFER_USDT_TO_MARGIN_ASSET_URI,
    method=HttpRequestMethod.POST,
    function_handler=server_post_responder,
)
"""Endpoint for transferring USDT from wallet to margin asset"""
TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_ENDPOINT: Endpoint = Endpoint(
    uri=TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_URI,
    method=HttpRequestMethod.POST,
    function_handler=server_post_responder,
)
"""Endpoint for transferring USDT from margin asset to wallet"""
ALL_ENDPOINTS: list[Endpoint] = [
    OPEN_MARGIN_ORDER_ENDPOINT,
    GET_SYMBOL_DETAILS_ENDPOINT,
    SET_SL_TP_FOR_MARGIN_ORDER_ENDPOINT,
    GET_WALLET_USDT_BALANCE_ENDPOINT,
    TRANSFER_USDT_TO_MARGIN_ASSET_ENDPOINT,
    TRANSFER_USDT_FROM_MARGIN_ASSET_TO_WALLET_ENDPOINT,
    GET_ORDERS_HISTORY_ENDPOINT,
    GET_ALL_MARGIN_OPEN_ORDERS_ENDPOINT,
    GET_MARGIN_ASSET_DETAILS_ENDPOINT,
    GET_ACCOUNT_PREFERENCES_ENDPOINT,
    BASE_TEST_GET_ENDPOINT,
    BASE_TEST_POST_ENDPOINT,
    UNKNOWN_ENDPOINT,
]
"""List of all Endpoints"""
# endregion ENDPOINTS


async def start_web_server(aiohttp_server) -> test_utils.TestServer:
    """Creates a test web server and returns it.

    Args:
        aiohttp_server (_type_): aiohttp_server received by test function

    Returns:
        test_utils.TestServer: A pre-configured test server
    """
    # Create a web server
    app: web.Application = web.Application()

    # Add routings
    for endpoint in ALL_ENDPOINTS:
        if endpoint.method is HttpRequestMethod.GET:
            app.router.add_get(
                path=endpoint.uri,
                handler=endpoint.function_handler,
            )
        else:
            app.router.add_post(
                path=endpoint.uri,
                handler=endpoint.function_handler,
            )

    # Return the server
    server: test_utils.TestServer = await aiohttp_server(app, port=TEST_SERVER_PORT)
    return server


async def create_tabdeal_client(client_session: aiohttp.ClientSession) -> TabdealClient:
    """Creates the TabdealClient object and returns it.

    Args:
        client_session (aiohttp.ClientSession): aiohttp client session

    Returns:
        TabdealClient: TabdealClient object
    """
    return TabdealClient(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
        client_session=client_session,
    )
