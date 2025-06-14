"""This file contains tests for the tabdeal_client module."""
# ruff: noqa: S101, ANN001, F841, E501, SLF001
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type"
# pylint: disable=W0613,W0612,C0301,W0212

from typing import TYPE_CHECKING

from tests.test_constants import EXPECTED_SESSION_HEADERS
from tests.test_helper_functions import create_tabdeal_client

if TYPE_CHECKING:
    from unofficial_tabdeal_api.tabdeal_client import TabdealClient


async def test_init() -> None:
    """Tests the initialization of an object from tabdeal_client class."""
    # Create an object using test data
    test_tabdeal: TabdealClient = await create_tabdeal_client()

    # Check attributes
    # Check if session headers is stored correctly
    assert test_tabdeal._client_session.headers == EXPECTED_SESSION_HEADERS

    # Check the test function
    assert await test_tabdeal._test() == "test"
