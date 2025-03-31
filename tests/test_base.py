"""This file is for testing functions of base module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,type-arg,import-untyped"
# pylint: disable=W0212,W0612,C0301

from aiohttp import ClientSession, test_utils, web

from tests.test_constants import (
    ERROR_POST_DATA_TO_SERVER_RESPONSE,
    EXPECTED_CORRECT_GET_RESPONSE_TEXT,
    EXPECTED_SESSION_HEADERS,
    INVALID_POST_CONTENT,
    INVALID_USER_AUTH_KEY,
    INVALID_USER_HASH,
    STATUS_BAD_REQUEST,
    STATUS_UNAUTHORIZED,
    TEST_POST_CONTENT,
    TEST_SERVER_ADDRESS,
    TEST_URI_PATH,
    TEST_URI_SUCCESS_CONTENT,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import server_maker
from unofficial_tabdeal_api.base import BaseClass


async def test_init() -> None:
    """Tests the initialization of an object from base class."""
    # Create an empty aiohttp.ClientSession object
    async with ClientSession() as client_session:
        # Create an object using test data
        test_base_object: BaseClass = BaseClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        # Check attributes
        # Check if session is stored correctly
        assert test_base_object._client_session == client_session
        # Check if session headers is stored correctly
        assert test_base_object._session_headers == EXPECTED_SESSION_HEADERS


async def test_get_data_from_server(aiohttp_server) -> None:
    """Tests the get_data_from_server function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_get_responder,
    )

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_base_object: BaseClass = BaseClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        # GET sample data from server
        response = await test_base_object._get_data_from_server(TEST_URI_PATH)
        # Check response content is okay
        assert response == EXPECTED_CORRECT_GET_RESPONSE_TEXT

    # Check invalid requests
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        invalid_base_object: BaseClass = BaseClass(
            INVALID_USER_HASH,
            INVALID_USER_AUTH_KEY,
            client_session,
        )

        # Check invalid user hash and authorization key
        response = await invalid_base_object._get_data_from_server(TEST_URI_PATH)
        assert response is None

        # Check invalid request method
        response = await invalid_base_object._post_data_to_server(TEST_URI_PATH, TEST_POST_CONTENT)
        assert response == ERROR_POST_DATA_TO_SERVER_RESPONSE


async def test_post_data_to_server(aiohttp_server) -> None:
    """Tests the post_data_to_server function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.POST,
        server_post_responder,
    )

    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_base_object: BaseClass = BaseClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        # POST sample data to server
        response_status, response_content = await test_base_object._post_data_to_server(
            TEST_URI_PATH,
            TEST_POST_CONTENT,
        )

        # Check response status is okay
        assert response_status is True

        # Check response content is okay
        assert response_content == TEST_URI_SUCCESS_CONTENT

        # Check invalid POST content
        response = await test_base_object._post_data_to_server(TEST_URI_PATH, INVALID_POST_CONTENT)
        assert response == ERROR_POST_DATA_TO_SERVER_RESPONSE

    # Check invalid requests
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        invalid_base_object: BaseClass = BaseClass(
            INVALID_USER_HASH,
            INVALID_USER_AUTH_KEY,
            client_session,
        )

        # Check invalid user hash and authorization key
        response = await invalid_base_object._post_data_to_server(TEST_URI_PATH, TEST_POST_CONTENT)
        assert response == ERROR_POST_DATA_TO_SERVER_RESPONSE

        # Check invalid request method
        response = await invalid_base_object._get_data_from_server(TEST_URI_PATH)
        assert response is None


async def server_get_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server."""
    # Check if the request header is correct
    user_hash: str | None = request.headers.get("user-hash")
    user_auth_key: str | None = request.headers.get("Authorization")
    if (user_hash != TEST_USER_HASH) or (user_auth_key != TEST_USER_AUTH_KEY):
        return web.Response(
            status=STATUS_UNAUTHORIZED,
            text=f"Got invalid authentication headers.\nHash:{user_hash}\nAuth key:{user_auth_key}",
        )

    # Else, the headers and request type is correct
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
