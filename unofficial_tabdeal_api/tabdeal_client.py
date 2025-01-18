"""This is the class of Tabdeal client"""

# pylint: disable=broad-exception-caught
# TODO: fix this at a later time ^^^

import json
from logging import Logger
import logging
from typing import Any
import aiohttp

from unofficial_tabdeal_api import utils
from unofficial_tabdeal_api.constants import (
    GET_MARGIN_ASSET_DETAILS_PRT1,
    GET_MARGIN_ASSET_DETAILS_PRT2,
)


class TabdealClient:
    """a client class to communicate with Tabdeal platform"""

    def __init__(self, user_hash: str, authorization_key: str, client_session: aiohttp.ClientSession):

        self.__client_session: aiohttp.ClientSession = client_session
        self.__logger: Logger = logging.getLogger(__name__)
        self.__session_headers: dict[str, str] = utils.create_session_headers(user_hash, authorization_key)

    # region Base functions
    async def __get_data_from_server(
        self, connection_url: str
    ) -> dict[str, Any] | list[dict[str, Any]] | None:
        """Gets data from specified url and returns the parsed json back

        Returns [None] in case of an error

        Args:
            connection_url (str): Url of the server to get data from

        Returns:
            dict[str, Any] | list[dict[str, Any]] | None: a Dictionary, a list of dictionaries or None in case of an error
        """

        try:
            # Using session, first we GET data from server
            async with self.__client_session.get(url=connection_url, headers=self.__session_headers) as server_response:

                # If response status is NOT [200], that means there was a problem with the request
                # and we should cancel the process here and return [None]
                if server_response.status != 200:
                    self.__logger.warning(
                        "Server responded with invalid status code [%s] and content:\n%s",
                        server_response.status,
                        await server_response.text(),
                    )

                    return None

                # Else, the server response must be OK and status [200]
                # so we continue with parsing the response json
                json_string: str = await server_response.text()
                response_data = json.loads(json_string)

            # Finally, after successful parsing of json, we close the session
            # and return the data
            await self.__client_session.close()
            return response_data

        # If an error occurs, we close the session and return [None]
        except Exception as exception:
            self.__logger.exception(
                "Error occurred while trying to get data from server with url -> [%s]\nException data:\n%s\nReturning [None]",
                connection_url,
                exception,
            )

            await self.__client_session.close()
            return None

    # endregion Base functions

    async def get_margin_asset_id(self, isolated_symbol: str) -> int:
        """Gets the ID of a margin asset from server and returns it as an integer

        Returns `-1` in case of an error

        Args:
            isolated_symbol (str): Isolated symbol of margin asset. example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            int: Margin asset ID as integer
        """

        self.__logger.debug("Trying to get margin asset ID for [%s]", isolated_symbol)

        connection_url: str = (
            GET_MARGIN_ASSET_DETAILS_PRT1
            + isolated_symbol
            + GET_MARGIN_ASSET_DETAILS_PRT2
        )

        margin_asset_id: int

        # We get the data from server and save it in a temporary variable
        temp_variable = await self.__get_data_from_server(connection_url)

        # If the data from server is not what we expect, we print an error
        # and return [-1]
        if temp_variable is None:
            self.__logger.error(
                "Failed to get margin asset ID for [%s]. Server response is [None]! Returning [-1]",
                isolated_symbol,
            )

            return -1

        # Else, the server response must be OK
        # so we assign the asset ID and return it
        margin_asset_id = temp_variable["id"]  # type: ignore
        self.__logger.debug("Margin asset ID: [%s]", margin_asset_id)

        return margin_asset_id
