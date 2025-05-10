"""This is the class of Tabdeal client."""

from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.margin import MarginClass
from unofficial_tabdeal_api.wallet import WalletClass


class TabdealClient(AuthorizationClass, MarginClass, WalletClass):
    """a client class to communicate with Tabdeal platform."""
