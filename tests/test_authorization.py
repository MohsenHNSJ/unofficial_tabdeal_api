"""This file is for testing functions of authorization module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable"
# pylint: disable=W0613,W0612,C0301

import asyncio
import logging

import pytest
from aiohttp import ClientSession, test_utils, web

from tests.test_constants import (
    INVALID_SERVER_ADDRESS,
    INVALID_USER_AUTH_KEY,
    INVALID_USER_HASH,
    TEST_SERVER_ADDRESS,
    TEST_URI_SUCCESS_CONTENT,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import server_maker
from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.constants import GET_ACCOUNT_PREFERENCES_URI
from unofficial_tabdeal_api.enums import DryRun


async def test_is_authorization_key_valid(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the is_authorization_key_valid function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_authorization_valid_responder,
        GET_ACCOUNT_PREFERENCES_URI,
    )

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_authorization_object: AuthorizationClass = AuthorizationClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        # GET sample data from server
        response = await test_authorization_object.is_authorization_key_valid()
        # Check response is okay
        assert response is True

    # Check Error
    async with ClientSession(base_url=INVALID_SERVER_ADDRESS) as client_session:
        exception_test_authorization_object: AuthorizationClass = AuthorizationClass(
            INVALID_USER_HASH,
            INVALID_USER_AUTH_KEY,
            client_session,
        )

        # Check error writing
        with caplog.at_level(logging.ERROR):
            response = await exception_test_authorization_object.is_authorization_key_valid()
            assert response is False
        assert "Authorization key is INVALID or EXPIRED!" in caplog.text


async def test_keep_authorization_key_alive(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the keep_authorization_key_alive function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server,
        HttpRequestMethod.GET,
        server_authorization_valid_responder,
        GET_ACCOUNT_PREFERENCES_URI,
    )

    # Check correct function
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_keep_alive_object: AuthorizationClass = AuthorizationClass(
            TEST_USER_HASH,
            TEST_USER_AUTH_KEY,
            client_session,
        )

        with caplog.at_level(logging.DEBUG):
            async with asyncio.TaskGroup() as task_group:
                # Create a task for dry-run
                keep_authorization_key_alive_dryrun_task = task_group.create_task(
                    test_keep_alive_object.keep_authorization_key_alive(
                        wait_time=1,
                        dryrun=DryRun.YES,
                    ),
                )

            assert "Authorization key is still valid." in caplog.text

    # Check error
    async with ClientSession(base_url=INVALID_SERVER_ADDRESS) as client_session:
        error_test_keep_alive_object: AuthorizationClass = AuthorizationClass(
            INVALID_USER_HASH,
            INVALID_USER_AUTH_KEY,
            client_session,
        )

        # Check error writing
        with caplog.at_level(logging.ERROR):
            async with asyncio.TaskGroup() as task_group:
                # Create a task to run the function
                # This function should fail in under 6 seconds
                keep_authorization_key_alive_task = task_group.create_task(
                    error_test_keep_alive_object.keep_authorization_key_alive(
                        wait_time=1,
                    ),
                )
        assert "Consecutive fails reached" in caplog.text


async def server_authorization_valid_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server for checking authorization."""
    # Return data as success
    return web.Response(text=TEST_URI_SUCCESS_CONTENT)
