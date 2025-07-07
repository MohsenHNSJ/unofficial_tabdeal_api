"""This module holds the AuthorizationClass."""

import asyncio

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import (
    AUTH_KEY_INVALIDITY_THRESHOLD,
    GET_ACCOUNT_PREFERENCES_URI,
)
from unofficial_tabdeal_api.enums import DryRun
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

    async def keep_authorization_key_alive(
        self,
        *,
        _wait_time: int = 3000,
        _dryrun: DryRun = DryRun.NO,
    ) -> None:
        """Keeps the Authorization key alive by periodically calling and using it.

        This function is made to be used as an ongoing Task

        Add to `asyncio.TaskGroup()` or similar ways

        If the key happens to be invalid for AUTH_KEY_INVALIDITY_THRESHOLD times in a row,
        the loop would stop.

        Args:
            _wait_time (int): Wait time in seconds. A value between 3000 and 3500 is preferable.
                Defaults to 3000
            _dryrun (DryRun): Run the loop only once for testing. Defaults to DryRun.NO
        """
        self._logger.debug(
            "Keep authorization key alive started. Will check the key every [%s] seconds",
            _wait_time,
        )

        consecutive_fails: int = 0

        # This is a loop to use the Authorization key once every (wait_time), so it will not expire
        # If the consecutive_fails is reached, the loop would exit and function should stop
        while consecutive_fails < AUTH_KEY_INVALIDITY_THRESHOLD:
            self._logger.debug("Waiting for [%s] seconds", _wait_time)
            # First we wait, as we have already checked the authorization key at the start.
            # This method's goal is to keep the key alive, not to check it.
            await asyncio.sleep(_wait_time)

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

            # Check for dry running
            if _dryrun is DryRun.YES:
                # If dry run, break the loop
                break

        # After loop completion, if the consecutive fails are equal or above the set threshold,
        # log an error
        if consecutive_fails >= AUTH_KEY_INVALIDITY_THRESHOLD:
            self._logger.error(
                "Consecutive fails reached [%s] times!\nCheck Authorization key!",
                AUTH_KEY_INVALIDITY_THRESHOLD,
            )
