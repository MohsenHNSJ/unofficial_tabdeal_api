"""This module holds the custom exceptions."""

# region Server errors


class Error(Exception):
    """Exception raised for an error."""

    def __init__(self, status_code: int) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
        """
        self.status_code = status_code


class AuthorizationError(Error):
    """Exception raised when Authorization token is invalid or expired."""

    def __init__(self, status_code: int) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
        """
        super().__init__(status_code)
        self.add_note(
            "Authorization token either invalid or expired\n"
            "Please obtain a new Authorization token.",
        )


class RequestError(Error):
    """Exception raised when the server could not understand the request."""

    def __init__(self, *, status_code: int, server_response: str) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
            server_response (str): Response from server describing the error
        """
        super().__init__(status_code)
        self.server_response = server_response
        self.add_note(
            "The server could not understand the request and sent the following response:\n"
            f"{self.server_response}",
        )


class MarketNotFoundError(RequestError):
    """Exception raised when requested market is not found on Tabdeal platform."""

    def __init__(self, *, status_code: int, server_response: str) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
            server_response (str): Response from server describing the error
        """
        super().__init__(status_code=status_code, server_response=server_response)
        self.add_note("Requested market is not found on Tabdeal platform")


class MarginTradingNotActiveError(RequestError):
    """Exception raised when requested market is not available for margin trading on Tabdeal."""

    def __init__(self, *, status_code: int, server_response: str) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
            server_response (str): Response from server describing the error
        """
        super().__init__(status_code=status_code, server_response=server_response)
        self.add_note(
            "Requested market is not available for margin trading on Tabdeal platform",
        )


class NotEnoughBalanceError(RequestError):
    """Exception raised when asset balance is insufficient to perform the requested order."""

    def __init__(self, *, status_code: int, server_response: str) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
            server_response (str): Response from server describing the error
        """
        super().__init__(status_code=status_code, server_response=server_response)
        self.add_note(
            "Insufficient balance in asset to open requested order.\nDeposit more balance first.",
        )


class NotEnoughCreditAvailableError(RequestError):
    """Exception raised when requested borrow amount is over available credit."""

    def __init__(self, *, status_code: int, server_response: str) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
            server_response (str): Response from server describing the error
        """
        super().__init__(status_code=status_code, server_response=server_response)
        self.add_note(
            "Requested borrow amount is over available credit.\nPlease reduce the borrow amount.",
        )


class RequestedParametersInvalidError(RequestError):
    """Exception raised when requested parameters are invalid."""

    def __init__(self, *, status_code: int, server_response: str) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
            server_response (str): Response from server describing the error
        """
        super().__init__(status_code=status_code, server_response=server_response)
        self.add_note(
            "Requested parameters are invalid.\nPlease check the parameters and try again.",
        )


class TransferAmountOverAccountBalanceError(RequestError):
    """Exception raised when requested transfer amount is over the account available balance."""

    def __init__(self, *, status_code: int, server_response: str) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
            server_response (str): Response from server describing the error
        """
        super().__init__(status_code=status_code, server_response=server_response)
        self.add_note(
            "Requested transfer amount is over the account available balance.\n"
            "Please reduce the transfer amount.",
        )


class TransferFromMarginAssetToWalletNotPossibleError(RequestError):
    """Exception raised when requested transfer is not possible due to unknown reason."""

    def __init__(self, *, status_code: int, server_response: str) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
            server_response (str): Response from server describing the error
        """
        super().__init__(status_code=status_code, server_response=server_response)
        self.add_note(
            "Requested transfer is not possible due to an unknown error!.\n"
            "Server did not provide any explanation!?",
        )


class MarginPositionNotFoundError(RequestError):
    """Exception raised when can't set SL/TP because margin position is not found."""

    def __init__(self, *, status_code: int, server_response: str) -> None:
        """Initializes the exception.

        Args:
            status_code (int): Status code received from the server
            server_response (str): Response from server describing the error
        """
        super().__init__(status_code=status_code, server_response=server_response)
        self.add_note(
            "Cannot set SL/TP points to requested margin asset.\n"
            "Does the margin asset has an active order?\n"
            "Is margin asset ID correct?\n"
            "Note: Server did not specify the problem :(",
        )


# endregion Server errors

# region Processing errors


class BreakEvenPriceNotFoundError(Exception):
    """Exception raised when break even price point is not found."""

    def __init__(self) -> None:
        """Initializes the exception."""
        self.add_note("Break even price point not found!\nIs order open?")


class OrderNotFoundInSpecifiedHistoryRangeError(Exception):
    """Exception raised when order is not found in specified history range."""

    def __init__(self) -> None:
        """Initializes the exception."""
        self.add_note(
            "Order not found in the specified history range!\n"
            "Is order ID correct? Check order ID first\n"
            "Is order too old? Try increasing the history range",
        )


class MarginOrderNotFoundInActiveOrdersError(Exception):
    """Exception raised when requested margin order is not in active orders list."""

    def __init__(self) -> None:
        """Initializes the exception."""
        self.add_note(
            "Order not found in active orders list!"
            "Is order ID correct?"
            "Maybe order is completed and hit either SL or TP points",
        )


# endregion Processing errors
