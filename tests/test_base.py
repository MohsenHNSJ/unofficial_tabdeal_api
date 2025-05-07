"""This file is for testing functions of base module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,type-arg,import-untyped,assignment,unreachable"
# pylint: disable=W0212,W0612,C0301

import logging
from typing import TYPE_CHECKING, Any

import pytest
from aiohttp import ClientSession, web

from tests.test_constants import (
    EXPECTED_CORRECT_GET_RESPONSE_TEXT,
    EXPECTED_SESSION_HEADERS,
    INVALID_POST_CONTENT,
    INVALID_USER_AUTH_KEY,
    INVALID_USER_HASH,
    STATUS_IM_A_TEAPOT,
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
from unofficial_tabdeal_api.constants import STATUS_BAD_REQUEST, STATUS_UNAUTHORIZED
from unofficial_tabdeal_api.exceptions import AuthorizationError, Error, RequestError

# Unused imports add a performance overhead at runtime, and risk creating import cycles.
# If an import is only used in typing-only contexts,
# it can instead be imported conditionally under an if TYPE_CHECKING: block to minimize runtime overhead.
if TYPE_CHECKING:  # pragma: no cover
    from aiohttp import test_utils


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
        with pytest.raises(AuthorizationError):
            response = await invalid_base_object._get_data_from_server(TEST_URI_PATH)


async def test_get_unknown_error_from_server(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the unknown error from server."""
    # Check unknown error
    invalid_server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_unknown_error_responder,
    )

    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_object: BaseClass = BaseClass(
            TEST_USER_AUTH_KEY,
            TEST_USER_HASH,
            client_session,
        )

        with caplog.at_level(logging.ERROR), pytest.raises(Error):
            response = await test_object._get_data_from_server(TEST_URI_PATH)
        assert "Server responded with invalid status code [418] and content:" in caplog.text


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
        response_content: (
            dict[str, Any] | list[dict[str, Any]]
        ) = await test_base_object._post_data_to_server(
            TEST_URI_PATH,
            TEST_POST_CONTENT,
        )

        if isinstance(response_content, dict):
            # Check response content is okay
            assert response_content["RESULT"] == "SUCCESS"
        else:
            pytest.fail(
                "The response from test server was not processed as a dictionary",
            )

        # Check invalid POST content for unknown error
        with pytest.raises(RequestError):
            response = await test_base_object._post_data_to_server(
                TEST_URI_PATH,
                INVALID_POST_CONTENT,
            )

    # Check invalid requests
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        invalid_base_object: BaseClass = BaseClass(
            INVALID_USER_HASH,
            INVALID_USER_AUTH_KEY,
            client_session,
        )

        # Check invalid user hash and authorization key
        with pytest.raises(AuthorizationError):
            response = await invalid_base_object._post_data_to_server(
                TEST_URI_PATH,
                TEST_POST_CONTENT,
            )


async def server_get_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server."""
    # Check if the request header is correct
    user_hash: str | None = request.headers.get("user-hash")
    user_auth_key: str | None = request.headers.get("Authorization")
    if (user_hash != TEST_USER_HASH) or (user_auth_key != TEST_USER_AUTH_KEY):
        return web.Response(
            status=STATUS_UNAUTHORIZED,
            text='{"detail":"Token is invalid or expired"}',
        )

    # Else, the headers and request type is correct
    return web.Response(text=TEST_URI_SUCCESS_CONTENT)


async def server_unknown_error_responder(request: web.Request) -> web.Response:
    """Returns an unknown error code from server (418 for example)."""
    return web.Response(
        status=STATUS_IM_A_TEAPOT,
        text=f"The requested entity body is short and stout.\nTip me over and pour me out.\nRequest Type: [{request.method}]",
    )


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
