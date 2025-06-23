"""This file is for testing functions of authorization module."""
# ruff: noqa: S101, ANN001
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable"
# pylint: disable=W0613,W0612,C0301

import asyncio
import logging
from typing import TYPE_CHECKING

import pytest
from aiohttp import ClientSession

from tests.test_constants import (
    INVALID_USER_AUTH_KEY,
    INVALID_USER_HASH,
    TEST_SERVER_ADDRESS,
)
from tests.test_helper_functions import create_tabdeal_client, start_web_server
from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.enums import DryRun

if TYPE_CHECKING:  # pragma: no cover
    from unofficial_tabdeal_api.tabdeal_client import TabdealClient


async def test_is_authorization_key_valid(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the is_authorization_key_valid function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Check correct request
    # Create an aiohttp.ClientSession object with base url set to test server
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        # Create an object using test data
        test_authorization_object: TabdealClient = await create_tabdeal_client(
            client_session=client_session,
        )

        with caplog.at_level(level=logging.DEBUG):
            # GET sample data from server
            response: bool = await test_authorization_object.is_authorization_key_valid()
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
        with caplog.at_level(level=logging.ERROR):
            response = await invalid_authorization_object.is_authorization_key_valid()
            assert response is False
        assert "Authorization key invalid or expired!" in caplog.text


async def test_keep_authorization_key_alive(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the keep_authorization_key_alive function."""
    # Start web server
    await start_web_server(aiohttp_server=aiohttp_server)

    # Check correct function
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_keep_alive_object: TabdealClient = await create_tabdeal_client(
            client_session=client_session,
        )

        with caplog.at_level(level=logging.DEBUG):
            async with asyncio.TaskGroup() as task_group:
                # Create a task for dry-run
                (
                    task_group.create_task(
                        coro=test_keep_alive_object.keep_authorization_key_alive(
                            wait_time=1,
                            dryrun=DryRun.YES,
                        ),
                    )
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
        with caplog.at_level(level=logging.ERROR):
            async with asyncio.TaskGroup() as task_group:
                # Create a task to run the function
                # This function should fail in under 6 seconds
                task_group.create_task(
                    coro=error_test_keep_alive_object.keep_authorization_key_alive(
                        wait_time=1,
                    ),
                )
        assert "Consecutive fails reached" in caplog.text
