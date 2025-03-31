"""This module holds the BaseClass."""

# pylint: disable=broad-exception-caught
# TODO: fix this at a later time ^^^

import json
import logging
from typing import Any

from aiohttp import ClientSession

from unofficial_tabdeal_api import constants, utils


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
    ) -> dict[str, Any] | list[dict[str, Any]] | None:
        """Gets data from specified url and returns the parsed json back.

        Returns `None` in case of an error

        Args:
            connection_url (str): Url of the server to get data from

        Returns:
            dict[str, Any] | list[dict[str, Any]] | None: a Dictionary, a list of dictionaries,
            `None` in case of an error
        """
        response_data = None

        try:
            # Using session, first we GET data from server
            async with self._client_session.get(
                url=connection_url,
                headers=self._session_headers,
            ) as server_response:
                # If response status is [200], we continue with parsing the response json
                if server_response.status == constants.STATUS_OK:
                    json_string: str = await server_response.text()
                    response_data = json.loads(json_string)

                else:
                    self._logger.warning(
                        "Server responded with invalid status code [%s] and content:\n%s",
                        server_response.status,
                        await server_response.text(),
                    )

        # If an error occurs, we close the session and return [None]
        except Exception:
            self._logger.exception(
                "Error occurred while trying to get data from server with url -> [%s]\n"
                "Exception data:\n"
                "Returning [None]",
                connection_url,
            )

        # Finally, we return the data
        return response_data

    async def _post_data_to_server(self, connection_url: str, data: str) -> tuple[bool, str | None]:
        """Posts data to specified url and returns the result of request.

        Returns a `tuple`, containing the status of operation and server response

        Returns `False` in case of an error

        Args:
            connection_url (str): Url of server to post data to
            data (str): Stringed json data to send to server

        Returns:
            tuple[bool, str]: a `tuple`, `bool` shows the success of request
            `str` returns the server response
        """
        operation_status: bool = False
        response_data = None

        try:
            # Using the session, First we POST data to server
            async with self._client_session.post(
                url=connection_url,
                headers=self._session_headers,
                data=data,
            ) as server_response:
                # If response status is [200], we continue with parsing the response json
                if server_response.status == constants.STATUS_OK:
                    operation_status = True
                    response_data = await server_response.text()
                else:
                    self._logger.warning(
                        "Server responded with invalid status code [%s] and content:\n%s",
                        server_response.status,
                        await server_response.text(),
                    )

        # If an error occurs, we close the session ans return [False]
        except Exception:
            self._logger.exception(
                "Error occurred while trying to post data to server with url -> [%s] and data:\n"
                "%s\n",
                connection_url,
                data,
            )
            self._logger.warning(
                "Returning status: [%s] with content:\n%s",
                operation_status,
                await server_response.text(),  # type: ignore[UnboundVariable]
            )

        # Finally, we return the data
        return operation_status, response_data
