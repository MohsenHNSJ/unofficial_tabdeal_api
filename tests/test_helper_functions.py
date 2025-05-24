"""This file contains helper functions used for testing only."""
# ruff: noqa: ANN001
# mypy: disable-error-code="no-untyped-def,type-arg"

from collections.abc import Callable

from aiohttp import test_utils, web

from tests.test_constants import TEST_SERVER_PORT, TEST_URI_PATH
from tests.test_enums import HttpRequestMethod
from tests.test_server import server_get_responder, server_post_responder
from unofficial_tabdeal_api.constants import (
    GET_MARGIN_ASSET_DETAILS_URI,
    OPEN_MARGIN_ORDER_URI,
    SET_SL_TP_FOR_MARGIN_ORDER_URI,
)


class Endpoint:
    """Endpoint class to hold endpoint data."""

    def __init__(self, *, uri: str, method: HttpRequestMethod, function_handler: Callable) -> None:
        """Initializes the Endpoint object.

        Args:
            uri (str): Endpoint URI
            method (HttpRequestMethod): HTTP request method
            function_handler (Callable): Function to handle the request
        """
        self.uri = uri
        self.method = method
        self.function_handler = function_handler


async def server_maker(
    *,
    aiohttp_server,
    http_request_method: HttpRequestMethod,
    function_to_call: Callable,
    uri_path: str = TEST_URI_PATH,
) -> test_utils.TestServer:
    """Creates a test web server and returns it.

    Args:
        aiohttp_server (_type_): aiohttp_server received by test function
        http_request_method (HttpRequestMethod): Http request method for routing
        function_to_call (Callable): Function to be called on client request
        uri_path (str, optional): Uri path to expect calling. Defaults to TEST_URI_PATH.

    Returns:
        test_utils.TestServer: A pre-configured test server
    """
    # Create a web server
    app: web.Application = web.Application()

    # Add routings
    if http_request_method is HttpRequestMethod.GET:
        app.router.add_get(uri_path, function_to_call)
    else:
        app.router.add_post(uri_path, function_to_call)

    # Return the server
    server: test_utils.TestServer = await aiohttp_server(app, port=TEST_SERVER_PORT)
    return server


# TODO(MohsenHNSJ): Use the enhanced server maker for all functions
# 291


async def enhanced_server_maker(
    *,
    aiohttp_server,
    endpoints: list[Endpoint],
) -> test_utils.TestServer:
    """Creates a test web server and returns it.

    Args:
        aiohttp_server (_type_): aiohttp_server received by test function
        endpoints (list[Endpoint]): List of endpoints to be added to the server

    Returns:
        test_utils.TestServer: A pre-configured test server
    """
    # Create a web server
    app: web.Application = web.Application()

    # Add routings
    for endpoint in endpoints:
        if endpoint.method is HttpRequestMethod.GET:
            app.router.add_get(endpoint.uri, endpoint.function_handler)
        else:
            app.router.add_post(endpoint.uri, endpoint.function_handler)

    # Return the server
    server: test_utils.TestServer = await aiohttp_server(app, port=TEST_SERVER_PORT)
    return server


# region ENDPOINTS
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
# endregion ENDPOINTS
