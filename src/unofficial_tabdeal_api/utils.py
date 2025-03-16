"""This module holds the utility functions needed by the TabdealClient class."""


def create_session_headers(user_hash: str, authorization_key: str) -> dict[str, str]:
    """Creates the header fo aiohttp client session.

    Args:
        user_hash (str): User hash
        authorization_key (str): User authorization key

    Returns:
        dict[str, str]: Client session header
    """
    session_headers: dict[str, str] = {
        "user-hash": user_hash,
        "Authorization": authorization_key,
    }

    return session_headers
