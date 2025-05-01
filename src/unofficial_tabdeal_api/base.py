"""This module holds the BaseClass."""

import logging
from typing import Any

from aiohttp import ClientResponse, ClientSession

from unofficial_tabdeal_api import constants, utils
from unofficial_tabdeal_api.exceptions import UserError


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

    async def _post_data_to_server(self, connection_url: str, data: str) -> str:
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

            # If we reach here, the response must be okay, so we return it
            return await server_response.text()

    async def _check_response(self, response: ClientResponse) -> None:
        """Check the server response and raise appropriate exception in case of an error.

        Args:
            response (ClientResponse): Response from server
        """
        self._logger.debug(
            "Response received with status code [%s]",
            response.status,
        )
        # If the status code is (200), everything is okay and we exit checking.
        if response.status == constants.STATUS_OK:
            return

        # Else, there must be problem with server response
        self._logger.exception(
            "Server responded with invalid status code [%s] and content:\n%s",
            response.status,
            await response.text(),
        )
        raise UserError(response.status)
