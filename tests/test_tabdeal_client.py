"""This file contains tests for the tabdeal_client module."""
# ruff: noqa: S101, ANN001, F841, E501, SLF001
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type"
# pylint: disable=W0613,W0612,C0301,W0212

from aiohttp import ClientSession

from tests.test_constants import EXPECTED_SESSION_HEADERS, TEST_USER_AUTH_KEY, TEST_USER_HASH
from unofficial_tabdeal_api.tabdeal_client import TabdealClient


async def test_init() -> None:
    """Tests the initialization of an object from tabdeal_client class."""
    # Create an empty aiohttp.ClientSession object
    async with ClientSession() as client_session:
        # Create an object using test data
        test_tabdeal_client_object: TabdealClient = await make_test_tabdeal_client_object(
            client_session,
        )

        # Check attributes
        # Check if session is stored correctly
        assert test_tabdeal_client_object._client_session == client_session
        # Check if session headers is stored correctly
        assert test_tabdeal_client_object._session_headers == EXPECTED_SESSION_HEADERS

        # Check the test function
        assert await test_tabdeal_client_object._test() == "test"


async def make_test_tabdeal_client_object(client_session: ClientSession) -> TabdealClient:
    """Creates a test object for testing TabdealClient."""
    return TabdealClient(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
        client_session=client_session,
    )
