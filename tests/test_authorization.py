"""This file is for testing functions of authorization module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped"
# pylint: disable=W0613,W0612,C0301

from aiohttp import ClientSession, test_utils, web

from tests.test_constants import (
    TEST_SERVER_ADDRESS,
    TEST_URI_SUCCESS_CONTENT,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import server_maker
from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.constants import GET_ACCOUNT_PREFERENCES_URI


async def test_is_authorization_key_valid(aiohttp_server) -> None:
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


async def server_authorization_valid_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server for checking authorization."""
    # Return data as success
    return web.Response(text=TEST_URI_SUCCESS_CONTENT)
