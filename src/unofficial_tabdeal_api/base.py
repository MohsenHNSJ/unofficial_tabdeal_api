"""This module holds the BaseClass."""
# pylint: disable=C0301

import logging
import types
from typing import Any, Self

from aiohttp import ClientResponse, ClientSession

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
        _is_test: bool = False,
    ) -> None:
        """Initializes the BaseClass with the given parameters.

        Args:
            user_hash (str): Unique identifier for the user
            authorization_key (str): Key used for authorizing requests
            _is_test (bool, optional): If True, the client will use test server. Defaults to False.
        """
        headers: dict[str, str] = {
            "user-hash": user_hash,
            "Authorization": authorization_key,
            "Content-Type": "application/json",
        }

        self._client_session: ClientSession
        # If _is_test is True, use the test server URL, otherwise use the base API URL
        if _is_test:
            self._client_session = ClientSession(
                base_url=constants.TEST_SERVER_URL,
                headers=headers,
            )
        else:
            self._client_session = ClientSession(
                base_url=constants.BASE_API_URL,
                headers=headers,
            )
        # Grab logger
        self._logger: logging.Logger = logging.getLogger(__name__)

    async def close(self) -> None:
        """Close the aiohttp client session."""
        if not self._client_session.closed:  # pragma: no cover
            await self._client_session.close()

    async def __aenter__(self) -> Self:
        """Enter the async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: types.TracebackType | None,
    ) -> None:
        """Exit the async context manager and close the session."""
        await self.close()

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
            dict[str, Any] | list[dict[str, Any]]: A Dictionary or a list of dictionaries.
        """
        # Using session, first we POST the data to server
        async with self._client_session.post(
            url=connection_url,
            data=data,
        ) as server_response:
            # We check the response here
            await self._check_response(server_response)

            # If we reach here, the response must be okay, so we process and return it
            return await utils.process_server_response(server_response)

    async def _check_response(self, response: ClientResponse) -> None:
        """Check the server response and raise appropriate exception in case of an error.

        Args:
            response (ClientResponse): Response from server

        Raises:
            AuthorizationError: Raised when the authorization key is invalid or expired
            Error: Raised for all other errors
        """
        self._logger.debug(
            "Response received with status code [%s]",
            response.status,
        )
        # Get server status and response
        server_status: int = response.status
        server_response: str = await response.text()
        # Check server status
        if server_status == constants.STATUS_OK:
            return
        if server_status == constants.STATUS_BAD_REQUEST:
            self._raise_specific_error(
                status_code=server_status,
                server_response=server_response,
            )
        if server_status == constants.STATUS_UNAUTHORIZED:
            raise AuthorizationError(status_code=server_status)
        # Else, we raise a generic error
        self._logger.exception(
            "Server responded with invalid status code [%s] and content:\n%s",
            server_status,
            server_response,
        )
        raise Error(status_code=server_status)

    def _raise_specific_error(self, status_code: int, server_response: str) -> None:
        """Raise a specific exception based on the server response content.

        Args:
            status_code (int): The status code of the response
            server_response (str): The content of the response

        Raises:
            exc_class: The specific exception class to raise
            RequestError: Raised for all other errors
        """
        error_map = {
            constants.MARKET_NOT_FOUND_RESPONSE: MarketNotFoundError,
            constants.MARGIN_NOT_ACTIVE_RESPONSE: MarginTradingNotActiveError,
            constants.NOT_ENOUGH_BALANCE_RESPONSE: NotEnoughBalanceError,
            constants.NOT_ENOUGH_CREDIT_AVAILABLE_RESPONSE: NotEnoughCreditAvailableError,
            constants.REQUESTED_PARAMETERS_INVALID_RESPONSE: RequestedParametersInvalidError,
            constants.TRANSFER_AMOUNT_OVER_ACCOUNT_BALANCE_RESPONSE: TransferAmountOverAccountBalanceError,  # noqa: E501
            constants.TRANSFER_FROM_MARGIN_ASSET_TO_WALLET_NOT_POSSIBLE_RESPONSE: TransferFromMarginAssetToWalletNotPossibleError,  # noqa: E501
            constants.MARGIN_POSITION_NOT_FOUND_RESPONSE: MarginPositionNotFoundError,
        }
        exc_class = error_map.get(server_response)
        if exc_class is not None:
            raise exc_class(
                status_code=status_code,
                server_response=server_response,
            )
        # Else, raise a generic RequestError
        raise RequestError(  # pragma: no cover
            status_code=status_code,
            server_response=server_response,
        )
