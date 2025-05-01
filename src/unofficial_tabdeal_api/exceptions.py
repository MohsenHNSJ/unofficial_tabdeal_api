"""This module holds the custom exceptions."""


class UserError(Exception):
    """Exception raised for a user error."""

    def __init__(self, status_code: int) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
        """
        self.status_code = status_code
