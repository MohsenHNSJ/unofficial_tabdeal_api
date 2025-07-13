"""This module holds the AuthorizationClass."""

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import (
    GET_ACCOUNT_PREFERENCES_URI,
)
from unofficial_tabdeal_api.exceptions import AuthorizationError


class AuthorizationClass(BaseClass):
    """This is the class storing methods related to Authorization."""

    async def is_authorization_key_valid(self) -> bool:
        """Checks the validity of provided authorization key.

        If the key is invalid or expired, return `False`

        If the key is working, return `True`

        Returns:
            bool: `True` or `False` based on the result
        """
        self._logger.debug("Checking Authorization key validity...")

        # First we get the data from server
        try:
            await self._get_data_from_server(connection_url=GET_ACCOUNT_PREFERENCES_URI)
        except AuthorizationError:
            # If we catch AuthorizationError, we return False
            self._logger.exception("Authorization key invalid or expired!")
            return False

        # If we reach here, the server response must be okay
        # So we return True
        self._logger.debug("Authorization key valid")
        return True
