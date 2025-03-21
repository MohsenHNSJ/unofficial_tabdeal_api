"""This file is for testing functions of base module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,type-arg"
# pylint: disable=W0212,W0612,C0301

from collections.abc import Callable

from aiohttp import ClientSession, test_utils, web

from tests.test_constants import (
    EXPECTED_SESSION_HEADERS,
    EXPECTED_TEST_GET_RESPONSE_TEXT,
    STATUS_BAD_REQUEST,
    STATUS_METHOD_NOT_ALLOWED,
    STATUS_UNAUTHORIZED,
    TEST_POST_CONTENT,
    TEST_SERVER_ADDRESS,
    TEST_SERVER_PORT,
    TEST_URI_PATH,
    TEST_URI_SUCCESS_CONTENT,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from unofficial_tabdeal_api.base import BaseClass


async def test_init() -> None:
    """Tests the initialization of an object from base class."""
    # Create an empty aiohttp.ClientSession object
    async with ClientSession() as client_session:

        # Create an object using test data
        test_base_object: BaseClass = BaseClass(
            TEST_USER_HASH, TEST_USER_AUTH_KEY, client_session)

        # Check attributes
        # Check if session is stored correctly
        assert test_base_object._client_session == client_session
        # Check if session headers is stored correctly
        assert test_base_object._session_headers == EXPECTED_SESSION_HEADERS


async def test_get_data_from_server(aiohttp_server) -> None:
    """Tests the get_data_from_server function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(aiohttp_server, HttpRequestMethod.GET, server_get_responder)

    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:

        # Create an object using test data
        test_base_object: BaseClass = BaseClass(
            TEST_USER_HASH, TEST_USER_AUTH_KEY, client_session)

        # GET sample data from server
        response = await test_base_object._get_data_from_server(TEST_URI_PATH)

        # Check response content is okay
        assert response == EXPECTED_TEST_GET_RESPONSE_TEXT


async def test_post_data_to_server(aiohttp_server) -> None:
    """Tests the post_data_to_server function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(aiohttp_server, HttpRequestMethod.POST, server_post_responder)

    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:

        # Create an object using test data
        test_base_object: BaseClass = BaseClass(
            TEST_USER_HASH, TEST_USER_AUTH_KEY, client_session)

        # POST sample data to server
        response_status, response_content = await test_base_object._post_data_to_server(TEST_URI_PATH, TEST_POST_CONTENT)

        # Check response status is okay
        assert response_status is True

        # Check response content is okay
        assert response_content == TEST_URI_SUCCESS_CONTENT


async def server_get_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server."""
    # Check if request type is correct
    if request.method != "GET":
        return web.Response(status=STATUS_METHOD_NOT_ALLOWED, text=f"Expected (GET) method, got {request.method} instead")
    # Check if the request header is correct
    user_hash: str | None = request.headers.get("user-hash")
    user_auth_key: str | None = request.headers.get("Authorization")
    if (user_hash != TEST_USER_HASH) or (user_auth_key != TEST_USER_AUTH_KEY):
        return web.Response(status=STATUS_UNAUTHORIZED, text=f"Got invalid authentication headers!\nHash:{user_hash}\nAuth key:{user_auth_key}")

    # Else, the headers and request type is correct
    return web.Response(text=TEST_URI_SUCCESS_CONTENT)


async def server_post_responder(request: web.Request) -> web.Response:
    """Mocks the POST response from server."""
    # Check if request type is correct
    if request.method != "POST":
        return web.Response(status=STATUS_METHOD_NOT_ALLOWED, text=f"Expected (POST) method, got {request.method} instead")
    # Check if the request header is correct
    user_hash: str | None = request.headers.get("user-hash")
    user_auth_key: str | None = request.headers.get("Authorization")
    if (user_hash != TEST_USER_HASH) or (user_auth_key != TEST_USER_AUTH_KEY):
        return web.Response(status=STATUS_UNAUTHORIZED, text=f"Got invalid authentication headers!\nHash:{user_hash}\nAuth key:{user_auth_key}")
    # Check if the content is correct
    if await request.text() != TEST_POST_CONTENT:
        return web.Response(status=STATUS_BAD_REQUEST, text=f"Expected:{TEST_POST_CONTENT}\nGot:{await request.text()}")

    # Else, the headers, request type and content is correct
    return web.Response(text=TEST_URI_SUCCESS_CONTENT)


async def server_maker(aiohttp_server, http_request_method: HttpRequestMethod, function_to_call: Callable) -> test_utils.TestServer:
    """Creates a test web server and returns it.

    Args:
        aiohttp_server (_type_): aiohttp_server received by test function
        http_request_method (HttpRequestMethod): Http request method for routing
        function_to_call (Callable): Function to be called on client request

    Returns:
        test_utils.TestServer: A pre-configured test server
    """
    # Create a web server
    app: web.Application = web.Application()

    # Add routings
    if http_request_method is HttpRequestMethod.GET:
        app.router.add_get(TEST_URI_PATH, function_to_call)
    else:
        app.router.add_post(TEST_URI_PATH, function_to_call)

    # Return the server
    server: test_utils.TestServer = await aiohttp_server(app, port=TEST_SERVER_PORT)
    return server
