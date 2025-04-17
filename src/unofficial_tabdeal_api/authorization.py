"""This module holds the AuthorizationClass."""

import asyncio

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import (
    AUTH_KEY_INVALIDITY_THRESHOLD,
    GET_ACCOUNT_PREFERENCES_URI,
)


class AuthorizationClass(BaseClass):
    """This is the class storing methods related to Authorization."""

    async def is_authorization_key_valid(self) -> bool:
        """Checks the validity of provided authorization key.

        If the key is invalid or expired, return `False`

        If the key is working, return `True`

        Returns:
            bool: `True` or `False` based on the result
        """
        self._logger.debug("Checking Authorization key validity")

        # First we get the data from server
        response_data = await self._get_data_from_server(GET_ACCOUNT_PREFERENCES_URI)

        # If the server response is NOT [None], then the Authorization key must be valid
        if response_data is not None:
            self._logger.debug("Authorization key is valid")
            return True

        self._logger.error(
            "Authorization key is INVALID or EXPIRED!\n"
            "Please provide a valid Authorization key\n"
            "Returning [False]",
        )
        return False

    async def keep_authorization_key_alive(self, wait_time: int) -> None:
        """Keeps the Authorization key alive by periodically calling and using it.

        This function is made to be used as an ongoing Task

        Add to `asyncio.TaskGroup()` or similar ways

        If the key happens to be invalid for AUTH_KEY_INVALIDITY_THRESHOLD times in a row,
        the loop would stop.

        Args:
            wait_time (int): Wait time in seconds.a value between 3000 and 3500 is preferable.
        """
        self._logger.debug(
            "Keep authorization key alive started.Will check the key every [%s] seconds",
            wait_time,
        )

        consecutive_fails: int = 0

        # This is a loop to use the Authorization key once every (wait_time), so it will not expire
        # If the consecutive_fails is reached, the loop would exit and function should stop
        while consecutive_fails <= AUTH_KEY_INVALIDITY_THRESHOLD:
            self._logger.debug("Waiting for [%s] seconds", wait_time)
            # First we wait, as we have already checked the authorization key at the start.
            # This method's goal is to keep the key alive, not to check it.
            await asyncio.sleep(wait_time)

            # Then we call the checker method
            check_result: bool = await self.is_authorization_key_valid()

            # Lastly, we log the result and loop again
            if check_result:
                self._logger.debug("Authorization key is still valid.")
                # Reset the consecutive fails
                consecutive_fails = 0
            else:
                self._logger.error(
                    "Authorization key is INVALID or EXPIRED! Check result [%s]",
                    check_result,
                )
                # Add one to consecutive fails
                consecutive_fails += 1

        self._logger.error(
            "Consecutive fails reached [%s] times!\nCheck Authorization key!",
            AUTH_KEY_INVALIDITY_THRESHOLD,
        )
