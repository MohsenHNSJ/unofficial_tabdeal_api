"""This file is for testing functions of base module."""
# ruff: noqa: S101, ANN001, F841, E501, SLF001
# mypy: disable-error-code="no-untyped-def,type-arg,import-untyped,assignment,unreachable"
# pylint: disable=W0212,W0612,C0301

import logging
from typing import TYPE_CHECKING, Any

import pytest
from aiohttp import ClientSession

from tests.test_constants import (
    EXPECTED_CORRECT_GET_RESPONSE_TEXT,
    EXPECTED_SESSION_HEADERS,
    INVALID_POST_CONTENT,
    INVALID_USER_AUTH_KEY,
    INVALID_USER_HASH,
    TEST_POST_CONTENT,
    TEST_SERVER_ADDRESS,
    TEST_URI_PATH,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import server_maker
from tests.test_server import (
    server_get_responder,
    server_post_responder,
    server_unknown_error_responder,
)
from unofficial_tabdeal_api.base import BaseClass
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
        test_base_object: BaseClass = await make_test_base_object(client_session)

        # Check attributes
        # Check if session is stored correctly
        assert test_base_object._client_session == client_session
        # Check if session headers is stored correctly
        assert test_base_object._session_headers == EXPECTED_SESSION_HEADERS


async def test_get_data_from_server(aiohttp_server) -> None:
    """Tests the get_data_from_server function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server=aiohttp_server,
        http_request_method=HttpRequestMethod.GET,
        function_to_call=server_get_responder,
    )

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_base_object: BaseClass = await make_test_base_object(client_session)

        # GET sample data from server
        response = await test_base_object._get_data_from_server(connection_url=TEST_URI_PATH)
        # Check response content is okay
        assert response == EXPECTED_CORRECT_GET_RESPONSE_TEXT

    # Check invalid requests
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        invalid_base_object: BaseClass = BaseClass(
            user_hash=INVALID_USER_HASH,
            authorization_key=INVALID_USER_AUTH_KEY,
            client_session=client_session,
        )

        # Check invalid user hash and authorization key
        with pytest.raises(AuthorizationError):
            response = await invalid_base_object._get_data_from_server(connection_url=TEST_URI_PATH)


async def test_get_unknown_error_from_server(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the unknown error from server."""
    # Check unknown error
    invalid_server: test_utils.TestServer = await server_maker(
        aiohttp_server=aiohttp_server,
        http_request_method=HttpRequestMethod.GET,
        function_to_call=server_unknown_error_responder,
    )

    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_object: BaseClass = await make_test_base_object(client_session)

        with caplog.at_level(logging.ERROR), pytest.raises(Error):
            response = await test_object._get_data_from_server(connection_url=TEST_URI_PATH)
        assert "Server responded with invalid status code [418] and content:" in caplog.text


async def test_post_data_to_server(aiohttp_server) -> None:
    """Tests the post_data_to_server function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server=aiohttp_server,
        http_request_method=HttpRequestMethod.POST,
        function_to_call=server_post_responder,
    )

    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_base_object: BaseClass = await make_test_base_object(client_session)

        # POST sample data to server
        response_content: (
            dict[str, Any] | list[dict[str, Any]]
        ) = await test_base_object._post_data_to_server(
            connection_url=TEST_URI_PATH,
            data=TEST_POST_CONTENT,
        )

        if isinstance(response_content, dict):  # pragma: no cover
            # Check response content is okay
            assert response_content["RESULT"] == "SUCCESS"
        else:
            pytest.fail(  # pragma: no cover
                "The response from test server was not processed as a dictionary",
            )

        # Check invalid POST content for unknown error
        with pytest.raises(RequestError):
            response = await test_base_object._post_data_to_server(
                connection_url=TEST_URI_PATH,
                data=INVALID_POST_CONTENT,
            )

    # Check invalid requests
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        invalid_base_object: BaseClass = BaseClass(
            user_hash=INVALID_USER_HASH,
            authorization_key=INVALID_USER_AUTH_KEY,
            client_session=client_session,
        )

        # Check invalid user hash and authorization key
        with pytest.raises(AuthorizationError):
            response = await invalid_base_object._post_data_to_server(
                connection_url=TEST_URI_PATH,
                data=TEST_POST_CONTENT,
            )


async def make_test_base_object(client_session: ClientSession) -> BaseClass:
    """Creates a test base object."""
    return BaseClass(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
        client_session=client_session,
    )
