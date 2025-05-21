"""This is the class of Tabdeal client."""

from unofficial_tabdeal_api.authorization import AuthorizationClass
from unofficial_tabdeal_api.margin import MarginClass
from unofficial_tabdeal_api.order import OrderClass
from unofficial_tabdeal_api.wallet import WalletClass


class TabdealClient(AuthorizationClass, MarginClass, WalletClass, OrderClass):
    """a client class to communicate with Tabdeal platform."""

    async def _test(self) -> str:
        """Temporary test function."""
        return "test"
