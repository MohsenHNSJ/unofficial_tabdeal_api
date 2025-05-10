"""This file contains helper functions used for testing only."""
# ruff: noqa: ANN001
# mypy: disable-error-code="no-untyped-def,type-arg"

from collections.abc import Callable

from aiohttp import test_utils, web

from tests.test_constants import TEST_SERVER_PORT, TEST_URI_PATH
from tests.test_enums import HttpRequestMethod


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
