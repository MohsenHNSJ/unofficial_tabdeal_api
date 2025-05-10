"""This file is for testing functions of wallet module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type"
# pylint: disable=W0613,W0612,C0301,W0212

import logging
from typing import TYPE_CHECKING

import pytest
from aiohttp import ClientSession

from tests.test_constants import (
    SAMPLE_WALLET_USDT_BALANCE,
    TEST_SERVER_ADDRESS,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import server_maker
from tests.test_server import server_get_responder
from unofficial_tabdeal_api.constants import GET_WALLET_USDT_BALANCE_URI
from unofficial_tabdeal_api.wallet import WalletClass

# Unused imports add a performance overhead at runtime, and risk creating import cycles.
# If an import is only used in typing-only contexts,
# it can instead be imported conditionally under an if TYPE_CHECKING: block to minimize runtime overhead.
if TYPE_CHECKING:  # pragma: no cover
    from decimal import Decimal

    from aiohttp import test_utils


async def test_get_wallet_usdt_balance(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_wallet_usdt_balance function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server=aiohttp_server,
        http_request_method=HttpRequestMethod.GET,
        function_to_call=server_get_responder,
        uri_path=GET_WALLET_USDT_BALANCE_URI,
    )

    # Check correct request
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_wallet: WalletClass = WalletClass(
            user_hash=TEST_USER_HASH,
            authorization_key=TEST_USER_AUTH_KEY,
            client_session=client_session,
        )

        with caplog.at_level(logging.DEBUG):
            # Check response
            response: Decimal = await test_wallet.get_wallet_usdt_balance()
            assert response == SAMPLE_WALLET_USDT_BALANCE
        # Check logs are written
        assert "Trying to get wallet balance" in caplog.text
        assert (
            f"Wallet balance retrieved successfully, [{SAMPLE_WALLET_USDT_BALANCE}] $"
            in caplog.text
        )
