"""Unofficial Tabdeal API.
--------------------------

a Package to communicate with Tabdeal platform

:copyright: (c) 2025-present MohsenHNSJ
:license: MIT, see LICENSE for more details

"""  # noqa: D205

__title__ = "unofficial-tabdeal-api"
__author__ = "MohsenHNSJ"
__license__ = "MIT"
__copyright__ = "Copyright 2025-present MohsenHNSJ"
__version__ = "0.2.0"

from .authorization import AuthorizationClass
from .margin import MarginClass
from .order import MarginOrder, OrderClass
from .tabdeal_client import TabdealClient
from .wallet import WalletClass

__all__: list[str] = [
    "AuthorizationClass",
    "MarginClass",
    "MarginOrder",
    "OrderClass",
    "TabdealClient",
    "WalletClass",
]
