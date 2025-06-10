"""This module holds the BaseClass."""

# ruff: noqa: SLF001

import logging
from typing import Any

from aiohttp import ClientResponse, ClientSession
from yarl import URL

from unofficial_tabdeal_api import constants, utils
from unofficial_tabdeal_api.exceptions import (
    AuthorizationError,
    Error,
    MarginPositionNotFoundError,
    MarginTradingNotActiveError,
    MarketNotFoundError,
    NotEnoughBalanceError,
    NotEnoughCreditAvailableError,
    RequestedParametersInvalidError,
    RequestError,
    TransferAmountOverAccountBalanceError,
    TransferFromMarginAssetToWalletNotPossibleError,
)


class BaseClass:
    """This is the base class, stores GET and POST functions."""

    def __init__(
        self,
        *,
        user_hash: str,
        authorization_key: str,
        client_session: ClientSession,
    ) -> None:
        """Initializes the BaseClass with the given parameters.

        Args:
            user_hash (str): Unique identifier for the user
            authorization_key (str): Key used for authorizing requests
            client_session (ClientSession): aiohttp session for making requests
        """
        self._client_session: ClientSession = client_session
        self._session_headers: dict[str, str] = utils.create_session_headers(
            user_hash=user_hash,
            authorization_key=authorization_key,
        )
        self._logger: logging.Logger = logging.getLogger(__name__)
        # If base_url_origin is not set, that means we are in production environment
        # so we set base_url and base_url_origin
        if self._client_session._base_url_origin is None:
            self._logger.debug("Setting base URL to production API URL")
            # Set the base URL to the production API URL
            self._client_session._base_url = URL(constants.BASE_API_URL)
            # Set the base URL origin to the production API URL origin
            self._client_session._base_url_origin = self._client_session._base_url.origin()
        # Else, it's already set and we leave it as is

    async def _get_data_from_server(
        self,
        *,
        connection_url: str,
        queries: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Gets data from specified url and returns the parsed json back.

        Args:
            connection_url (str): Url of the server to get data from
            queries (dict[str, Any] | None, optional): a Dictionary of queries. Defaults to None.

        Returns:
            dict[str, Any] | list[dict[str, Any]]: a Dictionary or a list of dictionaries
        """
        # Using session, first we GET the data from server
        async with self._client_session.get(
            url=connection_url,
            headers=self._session_headers,
            params=queries,
        ) as server_response:
            # We check the response here
            await self._check_response(server_response)

            # If we reach here, the response must be okay, so we process and return it
            return await utils.process_server_response(server_response)

    async def _post_data_to_server(
        self,
        *,
        connection_url: str,
        data: str,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Posts data to specified url and returns the result of request.

        Args:
            connection_url (str): Url of server to post data to
            data (str): Stringed json data to send to server

        Returns:
            str: Server response as string
        """
        # Using session, first we POST the data to server
        async with self._client_session.post(
            url=connection_url,
            headers=self._session_headers,
            data=data,
        ) as server_response:
            # We check the response here
            await self._check_response(server_response)

            # If we reach here, the response must be okay, so we process and return it
            return await utils.process_server_response(server_response)

    # TODO(MohsenHNSJ): Reduce the complexity of this function at a later time
    # 292
    async def _check_response(self, response: ClientResponse) -> None:  # noqa: C901
        """Check the server response and raise appropriate exception in case of an error.

        Args:
            response (ClientResponse): Response from server
        """
        self._logger.debug(
            "Response received with status code [%s]",
            response.status,
        )
        server_status: int = response.status
        server_response: str = await response.text()

        # If the status code is (200), everything is okay and we exit checking.
        if server_status == constants.STATUS_OK:
            return
        # If the status code is (400), There must be a problem with request
        if server_status == constants.STATUS_BAD_REQUEST:
            # Check server response and raise corresponding exception
            match server_response:
                # If the requested market is not found
                case _ if server_response == constants.MARKET_NOT_FOUND_RESPONSE:
                    raise MarketNotFoundError(
                        status_code=server_status,
                        server_response=server_response,
                    )

                # If the requested market is not available for margin trading
                case _ if server_response == constants.MARGIN_NOT_ACTIVE_RESPONSE:
                    raise MarginTradingNotActiveError(
                        status_code=server_status,
                        server_response=server_response,
                    )

                # If the requested amount of order exceeds the available balance
                case _ if server_response == constants.NOT_ENOUGH_BALANCE_RESPONSE:
                    raise NotEnoughBalanceError(
                        status_code=server_status,
                        server_response=server_response,
                    )

                # If the requested borrow amount is over available credit
                case _ if server_response == constants.NOT_ENOUGH_CREDIT_AVAILABLE_RESPONSE:
                    raise NotEnoughCreditAvailableError(
                        status_code=server_status,
                        server_response=server_response,
                    )

                # If the requested parameters are invalid
                case _ if server_response == constants.REQUESTED_PARAMETERS_INVALID_RESPONSE:
                    raise RequestedParametersInvalidError(
                        status_code=server_status,
                        server_response=server_response,
                    )

                # If requested transfer amount is over the account available balance
                case _ if (
                    server_response == constants.TRANSFER_AMOUNT_OVER_ACCOUNT_BALANCE_RESPONSE
                ):
                    raise TransferAmountOverAccountBalanceError(
                        status_code=server_status,
                        server_response=server_response,
                    )

                # If transferring from margin asset to wallet is not possible for some reason
                case _ if (
                    server_response
                    == constants.TRANSFER_FROM_MARGIN_ASSET_TO_WALLET_NOT_POSSIBLE_RESPONSE
                ):
                    raise TransferFromMarginAssetToWalletNotPossibleError(
                        status_code=server_status,
                        server_response=server_response,
                    )

                # If margin asset does not have an active position to set SL/TP
                # OR If margin asset ID is incorrect to set SL/TP
                case _ if server_response == constants.MARGIN_POSITION_NOT_FOUND_RESPONSE:
                    raise MarginPositionNotFoundError(
                        status_code=server_status,
                        server_response=server_response,
                    )

                # Else, An unknown problem with request occurred
                case _:
                    raise RequestError(
                        status_code=server_status,
                        server_response=server_response,
                    )

        # If the status code is (401), Token is invalid or expired
        if server_status == constants.STATUS_UNAUTHORIZED:
            raise AuthorizationError(server_status)

        # Else, there must be an unknown problem
        self._logger.exception(
            "Server responded with invalid status code [%s] and content:\n%s",
            server_status,
            server_response,
        )
        raise Error(server_status)
