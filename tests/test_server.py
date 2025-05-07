"""This file is for holding test server functions."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable"
# pylint: disable=W0613,W0612,C0301

from aiohttp import web

from tests.test_constants import (
    STATUS_IM_A_TEAPOT,
    TEST_POST_CONTENT,
    TEST_URI_SUCCESS_CONTENT,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from unofficial_tabdeal_api.constants import STATUS_BAD_REQUEST, STATUS_UNAUTHORIZED


async def server_get_responder(request: web.Request) -> web.Response:
    """Mocks the GET response from server."""
    # Check if the request header is correct
    user_hash: str | None = request.headers.get("user-hash")
    user_auth_key: str | None = request.headers.get("Authorization")
    if (user_hash != TEST_USER_HASH) or (user_auth_key != TEST_USER_AUTH_KEY):
        return web.Response(
            status=STATUS_UNAUTHORIZED,
            text='{"detail":"Token is invalid or expired"}',
        )

    # Else, the headers and request type is correct
    return web.Response(text=TEST_URI_SUCCESS_CONTENT)


async def server_post_responder(request: web.Request) -> web.Response:
    """Mocks the POST response from server."""
    # Check if the request header is correct
    user_hash: str | None = request.headers.get("user-hash")
    user_auth_key: str | None = request.headers.get("Authorization")
    if (user_hash != TEST_USER_HASH) or (user_auth_key != TEST_USER_AUTH_KEY):
        return web.Response(
            status=STATUS_UNAUTHORIZED,
            text=f"Got invalid authentication headers.\nHash:{user_hash}\nAuth key:{user_auth_key}",
        )
    # Check if the content is correct
    if await request.text() != TEST_POST_CONTENT:
        return web.Response(
            status=STATUS_BAD_REQUEST,
            text=f"Expected:{TEST_POST_CONTENT}\nGot:{await request.text()}",
        )

    # Else, the headers, request type and content is correct
    return web.Response(text=TEST_URI_SUCCESS_CONTENT)


async def server_unknown_error_responder(request: web.Request) -> web.Response:
    """Returns an unknown error code from server (418 for example)."""
    return web.Response(
        status=STATUS_IM_A_TEAPOT,
        text=f"The requested entity body is short and stout.\nTip me over and pour me out.\nRequest Type: [{request.method}]",
    )
