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
    SAMPLE_TRANSFER_USDT,
    SAMPLE_WALLET_USDT_BALANCE,
    TEST_ISOLATED_SYMBOL,
    TEST_SERVER_ADDRESS,
    TEST_TRUE,
)
from tests.test_helper_functions import create_tabdeal_client, start_web_server
from unofficial_tabdeal_api.exceptions import (
    MarketNotFoundError,
    TransferAmountOverAccountBalanceError,
    TransferFromMarginAssetToWalletNotPossibleError,
)

# Unused imports add a performance overhead at runtime, and risk creating import cycles.
# If an import is only used in typing-only contexts,
# it can instead be imported conditionally under an if TYPE_CHECKING: block to minimize runtime overhead.
if TYPE_CHECKING:  # pragma: no cover
    from aiohttp import test_utils

    from unofficial_tabdeal_api.tabdeal_client import TabdealClient


async def test_get_wallet_usdt_balance(aiohttp_server, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the get_wallet_usdt_balance function."""
    # Start web server
    server: test_utils.TestServer = await start_web_server(aiohttp_server=aiohttp_server)

    # Create client session
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_wallet: TabdealClient = await create_tabdeal_client(client_session=client_session)

        # Check valid request
        with caplog.at_level(level=logging.DEBUG):
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
        client_session.headers.add(
            key=RAISE_EXCEPTION_TEST_HEADER,
            value=TEST_TRUE,
        )
        # Create invalid object
        invalid_object: TabdealClient = await create_tabdeal_client(client_session=client_session)
        with pytest.raises(expected_exception=MarketNotFoundError):
            # Check response
            response = await invalid_object.get_wallet_usdt_balance()

        # Check invalid type response
        # Remove raise exception header
        client_session.headers.pop(RAISE_EXCEPTION_TEST_HEADER)
        # Add invalid type test header
        client_session.headers.add(
            key=INVALID_TYPE_TEST_HEADER,
            value=TEST_TRUE,
        )
        # Create invalid object
        invalid_type_object: TabdealClient = await create_tabdeal_client(
            client_session=client_session,
        )
        with caplog.at_level(level=logging.ERROR) and pytest.raises(expected_exception=TypeError):
            # Check response
            response = await invalid_type_object.get_wallet_usdt_balance()
        assert "Expected dictionary, got [<class 'list'>]" in caplog.text


async def test_transfer_usdt_from_wallet_to_margin_asset(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the transfer_usdt_from_wallet_to_margin_asset function."""
    # Start web server
    server: test_utils.TestServer = await start_web_server(
        aiohttp_server=aiohttp_server,
    )

    # Create client session
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_wallet: TabdealClient = await create_tabdeal_client(client_session=client_session)

        # Check valid request
        with caplog.at_level(level=logging.DEBUG):
            # Post request
            await test_wallet.transfer_usdt_from_wallet_to_margin_asset(
                transfer_amount=SAMPLE_TRANSFER_USDT,
                isolated_symbol=TEST_ISOLATED_SYMBOL,
            )
        # Check logs are written
        assert (
            f"Trying to transfer [{SAMPLE_TRANSFER_USDT}] USDT from wallet to margin asset [{TEST_ISOLATED_SYMBOL}]"
            in caplog.text
        )
        assert (
            f"Transfer of [{SAMPLE_TRANSFER_USDT}] USDT from wallet to margin asset [{TEST_ISOLATED_SYMBOL}] was successful"
            in caplog.text
        )

        # Check invalid request
        temp_amount: Decimal = Decimal(value=170)
        with pytest.raises(expected_exception=TransferAmountOverAccountBalanceError):
            # Post request
            await test_wallet.transfer_usdt_from_wallet_to_margin_asset(
                transfer_amount=temp_amount,
                isolated_symbol=TEST_ISOLATED_SYMBOL,
            )


async def test_transfer_usdt_from_margin_asset_to_wallet(
    aiohttp_server,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Tests the transfer_usdt_from_margin_asset_to_wallet function."""
    # Start web server
    server: test_utils.TestServer = await start_web_server(
        aiohttp_server=aiohttp_server,
    )

    # Create client session
    async with ClientSession(base_url=TEST_SERVER_ADDRESS) as client_session:
        test_wallet: TabdealClient = await create_tabdeal_client(client_session=client_session)

        # Check valid request
        with caplog.at_level(level=logging.DEBUG):
            # Post request
            await test_wallet.transfer_usdt_from_margin_asset_to_wallet(
                transfer_amount=SAMPLE_TRANSFER_USDT,
                isolated_symbol=TEST_ISOLATED_SYMBOL,
            )

        # Check logs are written
        assert (
            f"Trying to transfer [{SAMPLE_TRANSFER_USDT}] USDT from margin asset [{TEST_ISOLATED_SYMBOL}] to wallet"
            in caplog.text
        )
        assert (
            f"Transfer of [{SAMPLE_TRANSFER_USDT}] USDT from margin asset [{TEST_ISOLATED_SYMBOL}] to wallet was successful"
            in caplog.text
        )

        # Check invalid request
        temp_amount: Decimal = Decimal(value=250)
        with pytest.raises(expected_exception=TransferFromMarginAssetToWalletNotPossibleError):
            # Post request
            await test_wallet.transfer_usdt_from_margin_asset_to_wallet(
                transfer_amount=temp_amount,
                isolated_symbol=TEST_ISOLATED_SYMBOL,
            )
