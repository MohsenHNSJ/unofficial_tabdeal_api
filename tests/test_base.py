"""This file is for testing functions of base module."""
# ruff: noqa: S101, ANN001, E501, SLF001
# mypy: disable-error-code="no-untyped-def,type-arg,import-untyped,assignment,unreachable"
# pylint: disable=W0212,W0612,C0301

import logging
from typing import TYPE_CHECKING, Any

import pytest

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
    UNKNOWN_URI_PATH,
)
from tests.test_helper_functions import create_tabdeal_client, start_web_server
from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import BASE_API_URL
from unofficial_tabdeal_api.exceptions import AuthorizationError, Error, RequestError

# Unused imports add a performance overhead at runtime, and risk creating import cycles.
# If an import is only used in typing-only contexts,
# it can instead be imported conditionally under an if TYPE_CHECKING: block to minimize runtime overhead.
if TYPE_CHECKING:  # pragma: no cover
    from unofficial_tabdeal_api.tabdeal_client import TabdealClient


def test_init() -> None:
    """Tests the initialization of an object from base class."""
    # Create an object using test data
    test_base_object: TabdealClient = create_tabdeal_client()

    # Check if session headers is stored correctly
    assert test_base_object._client_session.headers == EXPECTED_SESSION_HEADERS
    # Check if session base URL is correct
    assert str(test_base_object._client_session._base_url) == TEST_SERVER_ADDRESS

    # Create an object using normal data
    normal_base_object: BaseClass = BaseClass(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
    )

    # Check if session base URL is correct
    assert str(normal_base_object._client_session._base_url) == BASE_API_URL


async def test_get_data_from_server(aiohttp_server) -> None:
    """Tests the get_data_from_server function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Check correct request
    # Create an object using test data
    test_base_object: TabdealClient = create_tabdeal_client()

    # GET sample data from server
    response: dict[str, Any] | list[dict[str, Any]] = await test_base_object._get_data_from_server(
        connection_url=TEST_URI_PATH,
    )
    # Check response content is okay
    assert response == EXPECTED_CORRECT_GET_RESPONSE_TEXT

    # Check invalid requests
    invalid_base_object: BaseClass = BaseClass(
        user_hash=INVALID_USER_HASH,
        authorization_key=INVALID_USER_AUTH_KEY,
        _is_test=True,  # Use test server
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

    test_object: TabdealClient = create_tabdeal_client()

    with caplog.at_level(level=logging.ERROR), pytest.raises(expected_exception=Error):
        await test_object._get_data_from_server(connection_url=UNKNOWN_URI_PATH)
    assert "Server responded with invalid status code [418] and content:" in caplog.text


async def test_post_data_to_server(aiohttp_server) -> None:
    """Tests the post_data_to_server function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Create an object using test data
    test_base_object: TabdealClient = create_tabdeal_client()

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
    invalid_base_object: BaseClass = BaseClass(
        user_hash=INVALID_USER_HASH,
        authorization_key=INVALID_USER_AUTH_KEY,
        _is_test=True,  # Use test server
    )

    # Check invalid user hash and authorization key
    with pytest.raises(expected_exception=AuthorizationError):
        await invalid_base_object._post_data_to_server(
            connection_url=TEST_URI_PATH,
            data=TEST_POST_CONTENT,
        )


@pytest.mark.asyncio
async def test_async_context_manager_and_close() -> None:
    """Test async context management and close method of BaseClass."""
    test_base = BaseClass(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
        _is_test=True,
    )
    # Test close() directly
    await test_base.close()
    assert test_base._client_session.closed

    # Test async context manager
    test_base2 = BaseClass(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
        _is_test=True,
    )
    async with test_base2 as b:
        assert b is test_base2
        assert not b._client_session.closed
    assert test_base2._client_session.closed
