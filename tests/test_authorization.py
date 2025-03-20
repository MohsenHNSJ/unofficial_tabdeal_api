"""This file is for testing functions of authorization module."""
# ruff: noqa: S101, ANN001
# mypy: disable-error-code="no-untyped-def"

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
