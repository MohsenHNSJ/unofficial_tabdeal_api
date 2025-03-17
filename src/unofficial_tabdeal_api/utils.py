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


async def create_session_headers_async(user_hash: str, authorization_key: str) -> dict[str, str]:
    """Creates the header fo aiohttp client session.

    :param user_hash: User hash
    :type user_hash: str
    :param authorization_key: User authorization key
    :type authorization_key: str
    :return: Client session header
    :rtype: dict[str, str]
    """
    session_headers: dict[str, str] = {
        "user-hash": user_hash,
        "Authorization": authorization_key,
    }

    return session_headers
