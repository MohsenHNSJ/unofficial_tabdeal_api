"""This module holds the BaseClass."""

import logging
from typing import Any

from aiohttp import ClientResponse, ClientSession

from unofficial_tabdeal_api import constants, utils
from unofficial_tabdeal_api.exceptions import (
    AuthorizationError,
    Error,
    MarginTradingNotActiveError,
    MarketNotFoundError,
    NotEnoughBalanceError,
    RequestError,
)


class BaseClass:
    """This is the base class, stores GET and POST functions."""

    def __init__(
        self,
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
            user_hash,
            authorization_key,
        )
        self._logger: logging.Logger = logging.getLogger(__name__)

    async def _get_data_from_server(
        self,
        connection_url: str,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Gets data from specified url and returns the parsed json back.

        Args:
            connection_url (str): Url of the server to get data from

        Returns:
            dict[str, Any] | list[dict[str, Any]]: a Dictionary or a list of dictionaries
        """
        # Using session, first we GET the data from server
        async with self._client_session.get(
            url=connection_url,
            headers=self._session_headers,
        ) as server_response:
            # We check the response here
            await self._check_response(server_response)

            # If we reach here, the response must be okay, so we process and return it
            return await utils.process_server_response(server_response)

    async def _post_data_to_server(
        self,
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

    async def _check_response(self, response: ClientResponse) -> None:
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
            # If the requested market is not found
            if server_response == constants.MARKET_NOT_FOUND_RESPONSE:
                raise MarketNotFoundError(server_status, server_response)

            # If the requested market is not available for margin trading
            if server_response == constants.MARGIN_NOT_ACTIVE_RESPONSE:
                raise MarginTradingNotActiveError(
                    server_status,
                    server_response,
                )

            # If the requested amount of order exceeds the available balance
            if server_response == constants.NOT_ENOUGH_BALANCE_RESPONSE:
                raise NotEnoughBalanceError(server_status, server_response)

            # Else, An unknown problem with request occurred
            raise RequestError(server_status, server_response)
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
