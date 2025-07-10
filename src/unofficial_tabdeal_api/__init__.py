"""Unofficial Tabdeal API.
--------------------------

A Package to communicate with the Tabdeal platform

:copyright: (c) 2025-present MohsenHNSJ
:license: MIT, see LICENSE for more details

"""  # noqa: D205

__title__ = "unofficial-tabdeal-api"
__author__ = "MohsenHNSJ"
__license__ = "MIT"
__copyright__ = "Copyright 2025-present MohsenHNSJ"
__version__ = "0.3.5"

from . import constants, enums, exceptions, models, utils
from .authorization import AuthorizationClass
from .base import BaseClass
from .margin import MarginClass
from .order import OrderClass
from .tabdeal_client import TabdealClient
from .wallet import WalletClass

__all__: list[str] = [
    "AuthorizationClass",
    "BaseClass",
    "MarginClass",
    "OrderClass",
    "TabdealClient",
    "WalletClass",
    "constants",
    "enums",
    "exceptions",
    "models",
    "utils",
]
