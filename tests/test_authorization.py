"""This file is for testing functions of authorization module."""
# ruff: noqa: S101, ANN001
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable"
# pylint: disable=W0613,W0612,C0301

import logging
from typing import TYPE_CHECKING

import pytest

from tests.test_constants import (
    INVALID_USER_AUTH_KEY,
    INVALID_USER_HASH,
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
    # Create an object using test data
    test_authorization_object: TabdealClient = create_tabdeal_client()

    with caplog.at_level(level=logging.DEBUG):
        # GET sample data from server
        response: bool = await test_authorization_object.is_authorization_key_valid()
        # Check response is okay
        assert response is True
    assert "Checking Authorization key validity..." in caplog.text
    assert "Authorization key valid" in caplog.text

    # Check invalid authentication
    invalid_authorization_object: AuthorizationClass = AuthorizationClass(
        user_hash=INVALID_USER_HASH,
        authorization_key=INVALID_USER_AUTH_KEY,
        _is_test=True,
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
    test_keep_alive_object: TabdealClient = create_tabdeal_client()

    with caplog.at_level(level=logging.DEBUG):
        await test_keep_alive_object.keep_authorization_key_alive(_wait_time=1, _dryrun=DryRun.YES)
        assert "Authorization key is still valid." in caplog.text

    # Check error
    error_test_keep_alive_object: AuthorizationClass = AuthorizationClass(
        user_hash=INVALID_USER_HASH,
        authorization_key=INVALID_USER_AUTH_KEY,
        _is_test=True,
    )

    # Check error writing
    with caplog.at_level(level=logging.ERROR):
        await error_test_keep_alive_object.keep_authorization_key_alive(_wait_time=1)
    assert "Consecutive fails reached" in caplog.text
