"""This is the base class, stores GET and POST functions"""

# pylint: disable=broad-exception-caught
# TODO: fix this at a later time ^^^

import json
import logging
from typing import Any
import aiohttp
from unofficial_tabdeal_api import utils
from unofficial_tabdeal_api.constants import GET_ACCOUNT_PREFERENCES_URL


class BaseClient:
    """This is the base class, stores GET and POST functions"""

    def __init__(
        self,
        user_hash: str,
        authorization_key: str,
        client_session: aiohttp.ClientSession,
    ):

        self._client_session: aiohttp.ClientSession = client_session
        self._session_headers: dict[str, str] = utils.create_session_headers(
            user_hash, authorization_key
        )
        self._logger: logging.Logger = logging.getLogger(__name__)

    async def _get_data_from_server(
        self, connection_url: str
    ) -> dict[str, Any] | list[dict[str, Any]] | None:
        """Gets data from specified url and returns the parsed json back

        Returns [None] in case of an error

        Args:
            connection_url (str): Url of the server to get data from

        Returns:
            dict[str, Any] | list[dict[str, Any]] | None: a Dictionary, a list of dictionaries or None in case of an error
        """
        response_data = None

        try:
            # Using session, first we GET data from server
            async with self._client_session.get(
                url=connection_url, headers=self._session_headers
            ) as server_response:

                # If response status is [200], we continue with parsing the response json
                if server_response.status == 200:

                    json_string: str = await server_response.text()
                    response_data = json.loads(json_string)

                else:
                    self._logger.warning(
                        "Server responded with invalid status code [%s] and content:\n%s",
                        server_response.status,
                        await server_response.text(),
                    )

        # If an error occurs, we close the session and return [None]
        except Exception as exception:
            self._logger.exception(
                "Error occurred while trying to get data from server with url -> [%s]\nException data:\n%s\nReturning [None]",
                connection_url,
                exception,
            )

        # Finally, we close the session and return the data
        await self._client_session.close()
        return response_data

    async def _post_data_to_server(
        self, connection_url: str, data: str
    ) -> tuple[bool, str]:
        """Posts data to specified url and returns the result of request

        Returns a tuple, containing the status of operation and server response

        Returns [False] in case of an error

        Args:
            connection_url (str): Url of server to post data to
            data (str): Stringed json data to send to server

        Returns:
            tuple[bool, str]: a Tuple, [bool] shows the success of request and [str] returns the server response
        """
        operation_status: bool = False

        try:
            # Using the session, First we POST data to server
            async with self._client_session.post(
                url=connection_url, data=data
            ) as server_response:

                # If response status is [200], we continue with parsing the response json
                if server_response.status == 200:

                    operation_status = True
                else:
                    self._logger.warning(
                        "Server responded with invalid status code [%s] and content:\n%s",
                        server_response.status,
                        await server_response.text(),
                    )

        # If an error occurs, we close the session ans return [False]
        except Exception as exception:
            self._logger.exception(
                "Error occurred while trying to post data to server with url -> [%s] and data:\n%s\nException details:\n%s",
                connection_url,
                data,
                exception,
            )
            self._logger.warning(
                "Returning status: [%s] with content:\n%s",
                operation_status,
                await server_response.text(),
            )

        # Finally, we close the session and return the data
        await self._client_session.close()
        return operation_status, await server_response.text()

    async def is_authorization_key_valid(self) -> bool:
        """Checks the validity of provided authorization key

        If the key is invalid or expired, return [False]

        If the key is working, return [True]

        Returns:
            bool: [True] or [False] based on the result
        """

        self._logger.debug("Checking Authorization key validity")

        # First we get the data from server
        response_data = await self._get_data_from_server(GET_ACCOUNT_PREFERENCES_URL)

        # If the server response is NOT [None], then the Authorization key must be valid
        if response_data is not None:
            self._logger.debug("Authorization key is valid")
            return True

        self._logger.error(
            "Authorization key is INVALID or EXPIRED!\nPlease provide a valid Authorization key\nReturning [False]"
        )
        return False
