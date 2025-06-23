"""This file is for testing functions of base module."""
# ruff: noqa: S101, ANN001, E501, SLF001
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
    UNKNOWN_URI_PATH,
)
from tests.test_helper_functions import create_tabdeal_client, start_web_server
from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.exceptions import AuthorizationError, Error, RequestError

# Unused imports add a performance overhead at runtime, and risk creating import cycles.
# If an import is only used in typing-only contexts,
# it can instead be imported conditionally under an if TYPE_CHECKING: block to minimize runtime overhead.
if TYPE_CHECKING:  # pragma: no cover
    from unofficial_tabdeal_api.tabdeal_client import TabdealClient


async def test_init() -> None:
    """Tests the initialization of an object from base class."""
    # Create an empty aiohttp.ClientSession object
    async with ClientSession() as client_session:
        # Create an object using test data
        test_base_object: TabdealClient = await create_tabdeal_client(client_session=client_session)

        # Check attributes
        # Check if session is stored correctly
        assert test_base_object._client_session == client_session
        # Check if session headers is stored correctly
        assert test_base_object._session_headers == EXPECTED_SESSION_HEADERS


async def test_get_data_from_server(aiohttp_server) -> None:
    """Tests the get_data_from_server function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_base_object: TabdealClient = await create_tabdeal_client(client_session=client_session)

        # GET sample data from server
        response: (
            dict[str, Any] | list[dict[str, Any]]
        ) = await test_base_object._get_data_from_server(connection_url=TEST_URI_PATH)
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
        with pytest.raises(expected_exception=AuthorizationError):
            await invalid_base_object._get_data_from_server(connection_url=TEST_URI_PATH)


async def test_get_unknown_error_from_server(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the unknown error from server."""
    # Check unknown error
    await start_web_server(aiohttp_server=aiohttp_server)

    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_object: TabdealClient = await create_tabdeal_client(client_session=client_session)

        with caplog.at_level(level=logging.ERROR), pytest.raises(expected_exception=Error):
            await test_object._get_data_from_server(connection_url=UNKNOWN_URI_PATH)
        assert "Server responded with invalid status code [418] and content:" in caplog.text


async def test_post_data_to_server(aiohttp_server) -> None:
    """Tests the post_data_to_server function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_base_object: TabdealClient = await create_tabdeal_client(client_session=client_session)

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
                reason="The response from test server was not processed as a dictionary",
            )

        # Check invalid POST content for unknown error
        with pytest.raises(expected_exception=RequestError):
            await test_base_object._post_data_to_server(
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
        with pytest.raises(expected_exception=AuthorizationError):
            await invalid_base_object._post_data_to_server(
                connection_url=TEST_URI_PATH,
                data=TEST_POST_CONTENT,
            )
