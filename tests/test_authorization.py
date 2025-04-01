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
    # Return data on success
    return web.Response(text=TEST_URI_SUCCESS_CONTENT)


# from aiohttp import ClientResponse, test_utils, web

# from tests.test_constants import STATUS_OK


# async def authorizer(request: web.Request) -> web.Response:
#     """Mocks the authorization response from server."""
#     return web.Response(text="TEST")


# async def test_is_authorization_key_valid(aiohttp_client) -> None:
#     """Tests the is_authorization_key_valid function."""
#     # Start web server
#     app: web.Application = web.Application()

#     # Add scenario
#     app.router.add_get("/r/", authorizer)

#     # Initialize client with the web server
#     client: test_utils.TestClient = await aiohttp_client(app)

#     # Receive response
#     response: ClientResponse = await client.get("/r/")

#     # Check response status
#     assert response.status == STATUS_OK

#     # Extract response data
#     text: str = await response.text()

#     # Check response data
#     assert "TEST" in text


# @pytest.mark.asyncio
# async def test_is_authorization_key_valid_2(aiohttp_client) -> None:

#     app = web.Application()

#     app.router.add_get(GET_ACCOUNT_PREFERENCES_URL, authorizer)

#     client_session = await aiohttp_client(app)

#     response: str = await client_session.get(GET_ACCOUNT_PREFERENCES_URL)

#     authorization_object: AuthorizationClass = AuthorizationClass(
#         TEST_USER_HASH, TEST_USER_AUTH_KEY, client_session)

#     response: bool = await authorization_object.is_authorization_key_valid()

#     assert await response is True
