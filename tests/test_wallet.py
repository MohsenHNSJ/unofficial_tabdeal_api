"""This file is for testing functions of wallet module."""
# ruff: noqa: S101, ANN001, F841, E501
# mypy: disable-error-code="no-untyped-def,import-untyped,unreachable,arg-type"
# pylint: disable=W0613,W0612,C0301,W0212

import logging
from decimal import Decimal
from typing import TYPE_CHECKING

import pytest
from aiohttp import ClientSession

from tests.test_constants import (
    INVALID_TYPE_TEST_HEADER,
    RAISE_EXCEPTION_TEST_HEADER,
    SAMPLE_TRANSFER_USDT_TO_MARGIN_ASSET,
    SAMPLE_WALLET_USDT_BALANCE,
    TEST_ISOLATED_SYMBOL,
    TEST_SERVER_ADDRESS,
    TEST_TRUE,
    TEST_USER_AUTH_KEY,
    TEST_USER_HASH,
)
from tests.test_enums import HttpRequestMethod
from tests.test_helper_functions import server_maker
from tests.test_server import server_get_responder, server_post_responder
from unofficial_tabdeal_api.constants import (
    GET_WALLET_USDT_BALANCE_URI,
    TRANSFER_USDT_TO_MARGIN_ASSET_URI,
)
from unofficial_tabdeal_api.exceptions import (
    MarketNotFoundError,
    TransferAmountOverAccountBalanceError,
)
from unofficial_tabdeal_api.wallet import WalletClass

# Unused imports add a performance overhead at runtime, and risk creating import cycles.
# If an import is only used in typing-only contexts,
# it can instead be imported conditionally under an if TYPE_CHECKING: block to minimize runtime overhead.
if TYPE_CHECKING:  # pragma: no cover
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

    # Create client session
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_wallet: WalletClass = await make_test_wallet_object(client_session)

        # Check valid request
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

        # Check invalid request
        # Add test header to raise exception
        client_session.headers.add(RAISE_EXCEPTION_TEST_HEADER, TEST_TRUE)
        # Create invalid object
        invalid_object: WalletClass = await make_test_wallet_object(client_session)
        with pytest.raises(MarketNotFoundError):
            # Check response
            response = await invalid_object.get_wallet_usdt_balance()

        # Check invalid type response
        # Remove raise exception header
        client_session.headers.pop(RAISE_EXCEPTION_TEST_HEADER)
        # Add invalid type test header
        client_session.headers.add(INVALID_TYPE_TEST_HEADER, TEST_TRUE)
        # Create invalid object
        invalid_type_object: WalletClass = await make_test_wallet_object(client_session)
        with caplog.at_level(logging.ERROR) and pytest.raises(TypeError):
            # Check response
            response = await invalid_type_object.get_wallet_usdt_balance()
        assert "Expected dictionary, got [<class 'list'>]" in caplog.text


async def test_transfer_usdt_from_wallet_to_margin_asset(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the transfer_usdt_from_wallet_to_margin_asset function."""
    # Start web server
    server: test_utils.TestServer = await server_maker(
        aiohttp_server=aiohttp_server,
        http_request_method=HttpRequestMethod.POST,
        function_to_call=server_post_responder,
        uri_path=TRANSFER_USDT_TO_MARGIN_ASSET_URI,
    )

    # Create client session
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_wallet: WalletClass = await make_test_wallet_object(client_session)

        # Check valid request
        with caplog.at_level(logging.DEBUG):
            # Post request
            await test_wallet.transfer_usdt_from_wallet_to_margin_asset(
                transfer_amount=SAMPLE_TRANSFER_USDT_TO_MARGIN_ASSET,
                isolated_symbol=TEST_ISOLATED_SYMBOL,
            )
        # Check logs are written
        assert (
            f"Trying to transfer [{SAMPLE_TRANSFER_USDT_TO_MARGIN_ASSET}] USDT from wallet to margin asset [{TEST_ISOLATED_SYMBOL}]"
            in caplog.text
        )
        assert (
            f"Transfer of [{SAMPLE_TRANSFER_USDT_TO_MARGIN_ASSET}] USDT from wallet to margin asset [{TEST_ISOLATED_SYMBOL}] was successful"
            in caplog.text
        )

        # Check invalid request
        temp_amount: Decimal = Decimal(170)
        with pytest.raises(TransferAmountOverAccountBalanceError):
            # Post request
            await test_wallet.transfer_usdt_from_wallet_to_margin_asset(
                transfer_amount=temp_amount,
                isolated_symbol=TEST_ISOLATED_SYMBOL,
            )


async def make_test_wallet_object(
    client_session: ClientSession,
) -> WalletClass:
    """Creates a test wallet object."""
    return WalletClass(
        user_hash=TEST_USER_HASH,
        authorization_key=TEST_USER_AUTH_KEY,
        client_session=client_session,
    )
