"""This is the class of Tabdeal client."""

from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.margin import MarginClass


class TabdealClient(AuthorizationClass, MarginClass):
    """a client class to communicate with Tabdeal platform."""
