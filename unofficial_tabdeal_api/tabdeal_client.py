"""This is the class of Tabdeal client"""

from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.constants import (
    GET_MARGIN_ASSET_DETAILS_PRT1,
    GET_MARGIN_ASSET_DETAILS_PRT2,
)


class TabdealClient(AuthorizationClass):
    """a client class to communicate with Tabdeal platform"""

    # region Margin
    async def get_margin_asset_id(self, isolated_symbol: str) -> int:
        """Gets the ID of a margin asset from server and returns it as an integer

        Returns `-1` in case of an error

        Args:
            isolated_symbol (str): Isolated symbol of margin asset. example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            int: Margin asset ID as integer
        """

        self._logger.debug("Trying to get margin asset ID for [%s]", isolated_symbol)

        connection_url: str = (
            GET_MARGIN_ASSET_DETAILS_PRT1
            + isolated_symbol
            + GET_MARGIN_ASSET_DETAILS_PRT2
        )

        margin_asset_id: int

        # We get the data from server and save it in a temporary variable
        temp_variable = await self._get_data_from_server(connection_url)

        # If the data from server is not what we expect, we print an error
        # and return [-1]
        if temp_variable is None:
            self._logger.error(
                "Failed to get margin asset ID for [%s]. Server response is [None]! Returning [-1]",
                isolated_symbol,
            )

            return -1

        # Else, the server response must be OK
        # so we assign the asset ID and return it
        margin_asset_id = temp_variable["id"]  # type: ignore
        self._logger.debug("Margin asset ID: [%s]", margin_asset_id)

        return margin_asset_id

    # endregion Margin
