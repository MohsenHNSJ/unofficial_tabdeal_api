"""This file is for testing functions of authorization module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable"
# pylint: disable=W0613,W0612,C0301

import asyncio
import logging

import pytest
from aiohttp import ClientSession, test_utils

from tests.test_constants import (
    INVALID_USER_AUTH_KEY,
    INVALID_USER_HASH,
    TEST_SERVER_ADDRESS,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import server_maker
from tests.test_server import server_get_responder
from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.constants import GET_ACCOUNT_PREFERENCES_URI
from unofficial_tabdeal_api.enums import DryRun


async def test_is_authorization_key_valid(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the is_authorization_key_valid function."""
    # Start web server
    server: test_utils.TestServer = await make_test_authorization_server(aiohttp_server)

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_authorization_object: AuthorizationClass = await make_test_authorization_object(
            client_session,
        )

        with caplog.at_level(logging.DEBUG):
            # GET sample data from server
            response = await test_authorization_object.is_authorization_key_valid()
            # Check response is okay
            assert response is True
        assert "Checking Authorization key validity..." in caplog.text
        assert "Authorization key valid" in caplog.text

    # Check invalid authentication
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        invalid_authorization_object: AuthorizationClass = AuthorizationClass(
            user_hash=INVALID_USER_HASH,
            authorization_key=INVALID_USER_AUTH_KEY,
            client_session=client_session,
        )

        # Check error writing
        with caplog.at_level(logging.ERROR):
            response = await invalid_authorization_object.is_authorization_key_valid()
            assert response is False
        assert "Authorization key invalid or expired!" in caplog.text


async def test_keep_authorization_key_alive(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the keep_authorization_key_alive function."""
    # Start web server
    server: test_utils.TestServer = await make_test_authorization_server(aiohttp_server)

    # Check correct function
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_keep_alive_object: AuthorizationClass = await make_test_authorization_object(
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
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        error_test_keep_alive_object: AuthorizationClass = AuthorizationClass(
            user_hash=INVALID_USER_HASH,
            authorization_key=INVALID_USER_AUTH_KEY,
            client_session=client_session,
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


async def make_test_authorization_object(client_session: ClientSession) -> AuthorizationClass:
    """Creates a test authorization object for testing AuthorizationClass."""
    return AuthorizationClass(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
        client_session=client_session,
    )


async def make_test_authorization_server(aiohttp_server) -> test_utils.TestServer:
    """Creates a test server for testing AuthorizationClass."""
    return await server_maker(
        aiohttp_server=aiohttp_server,
        http_request_method=HttpRequestMethod.GET,
        function_to_call=server_get_responder,
        uri_path=GET_ACCOUNT_PREFERENCES_URI,
    )
