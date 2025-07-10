"""This module holds the MarginClass."""

import json
from decimal import ROUND_DOWN, Decimal, getcontext, setcontext
from typing import TYPE_CHECKING, Any

from pydantic import ValidationError

from unofficial_tabdeal_api.base import BaseClass
from unofficial_tabdeal_api.constants import (
    DECIMAL_PRECISION,
    GET_ALL_MARGIN_OPEN_ORDERS_URI,
    GET_MARGIN_ASSET_DETAILS_URI,
    OPEN_MARGIN_ORDER_URI,
    ORDER_PLACED_SUCCESSFULLY_RESPONSE,
    SET_SL_TP_FOR_MARGIN_ORDER_URI,
)
from unofficial_tabdeal_api.enums import MathOperation, OrderSide, OrderState
from unofficial_tabdeal_api.exceptions import (
    BreakEvenPriceNotFoundError,
    MarginOrderNotFoundInActiveOrdersError,
    MarginTradingNotActiveError,
    MarketNotFoundError,
)
from unofficial_tabdeal_api.models import (
    IsolatedSymbolDetailsModel,
    MarginOpenOrderModel,
    MarginOrderModel,
)
from unofficial_tabdeal_api.utils import (
    calculate_order_volume,
    calculate_usdt,
    normalize_decimal,
)

# Unused imports add a performance overhead at runtime, and risk creating import cycles.
# If an import is only used in typing-only contexts,
# it can instead be imported conditionally under an if TYPE_CHECKING: block,
# to minimize runtime overhead.
if TYPE_CHECKING:  # pragma: no cover
    from decimal import Context

    from unofficial_tabdeal_api.models import (
        CurrencyCreditModel,
        PairModel,
    )


class MarginClass(BaseClass):
    """This is the class storing methods related to Margin trading."""

    async def get_isolated_symbol_details(self, isolated_symbol: str) -> IsolatedSymbolDetailsModel:
        """Gets the full details of an isolated symbol from server and returns it as a dictionary.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset.
            example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            IsolatedSymbolDetailsModel: A model containing isolated symbol details

        Raises:
            TypeError: If the response is not a dictionary
                or the response can't be validated.
        """
        self._logger.debug("Trying to get details of [%s]", isolated_symbol)

        # We create the connection query
        connection_query: dict[str, Any] = {
            "pair_symbol": isolated_symbol,
            "account_genre": "IsolatedMargin",
        }

        # We get the data from server
        server_response: dict[str, Any] | list[dict[str, Any]] = await self._get_data_from_server(
            connection_url=GET_MARGIN_ASSET_DETAILS_URI,
            queries=connection_query,
        )

        # If the response is not a dictionary, we log and raise a TypeError
        if not isinstance(server_response, dict):
            self._logger.error(
                "Expected dictionary, got [%s]",
                type(server_response),
            )

            raise TypeError

        # We try to convert the response into a pydantic model
        try:
            isolated_symbol_details = IsolatedSymbolDetailsModel(
                **server_response,
            )

            self._logger.debug(
                "Details retrieved successfully.\nSymbol name: [%s]",
                isolated_symbol_details.pair.symbol,
            )
        except (ValidationError, TypeError) as e:
            # If the data is not valid, we log and raise TypeError
            self._logger.exception(
                "Failed to validate isolated symbol details",
            )
            raise TypeError from e

        return isolated_symbol_details

    async def get_margin_all_open_orders(self) -> list[MarginOpenOrderModel]:
        """Gets all the open margin orders from server and returns it as a list of dictionaries.

        Returns:
            list[MarginOpenOrderModel]: a List of `MarginOpenOrderModel` items

        Raises:
            TypeError: If the response is not a list.
        """
        self._logger.debug("Trying to get all open margin orders")

        # We get the data from server
        server_response: dict[str, Any] | list[dict[str, Any]] = await self._get_data_from_server(
            connection_url=GET_ALL_MARGIN_OPEN_ORDERS_URI,
        )

        # if the response is not a list, we log and raise a TypeError
        if not isinstance(server_response, list):
            self._logger.error(
                "Expected list, got [%s]",
                type(server_response),
            )

            raise TypeError

        # We try to convert the response into a pydantic model
        try:
            list_of_open_orders: list[MarginOpenOrderModel] = [
                MarginOpenOrderModel(**item) for item in server_response
            ]

            self._logger.debug(
                "Data retrieved successfully.\nYou have [%s] open positions",
                len(list_of_open_orders),
            )

        except (ValidationError, TypeError) as e:
            # If the data is not valid, we log and raise TypeError
            self._logger.exception(
                "Failed to validate list of open margin orders",
            )

            raise TypeError from e

        return list_of_open_orders

    async def get_margin_asset_id(self, isolated_symbol: str) -> int:
        """Gets the ID of a margin asset from server and returns it as an integer.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset.
                example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            int: Margin asset ID as integer
        """
        self._logger.debug("Trying to get asset ID of [%s]", isolated_symbol)

        # We get the data from server
        isolated_symbol_details: IsolatedSymbolDetailsModel = (
            await self.get_isolated_symbol_details(isolated_symbol)
        )

        # We Extract the asset ID and return it
        margin_asset_id: int = isolated_symbol_details.id
        self._logger.debug("Margin asset ID: [%s]", margin_asset_id)

        return margin_asset_id

    async def get_order_break_even_price(self, asset_id: int) -> Decimal:
        """Gets the price point for an order which Tabdeal says it yields no profit and loss.

        Args:
            asset_id (int): Margin asset ID got from get_asset_id() function

        Returns:
            Decimal: The price as Decimal

        Raises:
            BreakEvenPriceNotFoundError: If no matching order is found.
        """
        self._logger.debug(
            "Trying to get break even price for margin asset with ID:[%s]",
            asset_id,
        )

        # First we get all margin open orders
        all_margin_open_orders: list[MarginOpenOrderModel] = await self.get_margin_all_open_orders()

        # Then we search through the list and find the asset ID we are looking for
        # And store that into our variable
        # Get the first object in a list that meets a condition, if nothing found, return [None]
        margin_order: MarginOpenOrderModel | None = None
        for order in all_margin_open_orders:
            if order.id == asset_id:
                margin_order = order
                break

        # If no match found in the server response, raise BreakEvenPriceNotFoundError
        if margin_order is None:
            self._logger.error(
                "Break even price not found for asset ID [%s]!",
                asset_id,
            )

            raise BreakEvenPriceNotFoundError

        # Else, we should have found a result, so we extract the break even price,
        # normalize and return it
        break_even_price: Decimal = normalize_decimal(
            margin_order.break_even_point,
        )

        self._logger.debug("Break even price found as [%s]", break_even_price)

        return break_even_price

    async def get_margin_pair_id(self, isolated_symbol: str) -> int:
        """Gets the pair ID for a margin asset from server and returns it as an integer.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset.
            example: BTCUSDT, MANAUSDT, BOMEUSDT, ...

        Returns:
            int: Margin pair ID as integer

        Raises:
            TypeError: If the response is not a dictionary.
        """
        self._logger.debug(
            "Trying to get margin pair ID of [%s]",
            isolated_symbol,
        )

        # We get the data from server
        isolated_symbol_details: IsolatedSymbolDetailsModel = (
            await self.get_isolated_symbol_details(isolated_symbol)
        )

        # We extract pair information
        margin_pair_information: PairModel = isolated_symbol_details.pair
        # Then we extract the pair ID and return it
        margin_pair_id: int = margin_pair_information.id
        self._logger.debug("Margin pair ID is [%s]", margin_pair_id)

        return margin_pair_id

    async def get_margin_asset_balance(self, isolated_symbol: str) -> Decimal:
        """Gets the margin asset balance in USDT from server and returns it as Decimal value.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset

        Returns:
            Decimal: Asset balance in USDT as Decimal

        Raises:
            TypeError: If the response is not a dictionary.
        """
        self._logger.debug(
            "Trying to get margin asset balance for [%s]",
            isolated_symbol,
        )

        # We get the data from server
        isolated_symbol_details: IsolatedSymbolDetailsModel = (
            await self.get_isolated_symbol_details(isolated_symbol)
        )

        # We extract margin asset balance
        margin_asset_usdt_details: CurrencyCreditModel = (
            isolated_symbol_details.second_currency_credit
        )
        margin_asset_usdt_balance: Decimal = normalize_decimal(
            margin_asset_usdt_details.available_amount,
        )
        self._logger.debug(
            "Margin asset [%s] balance is [%s]",
            isolated_symbol,
            margin_asset_usdt_balance,
        )

        return margin_asset_usdt_balance

    async def get_margin_asset_precision_requirements(
        self,
        isolated_symbol: str,
    ) -> tuple[int, int]:
        """Gets the precision requirements of an asset from server and returns it as a tuple.

        First return value is precision for volume.
        Second return value is precision for price.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset

        Returns:
            tuple[int, int]: A Tuple containing precision requirements for (1)volume and (2)price

        Raises:
            TypeError: If the response is not a dictionary.
        """
        self._logger.debug(
            "Trying to get precision requirements for asset [%s]",
            isolated_symbol,
        )

        # We get the data from server
        isolated_symbol_details: IsolatedSymbolDetailsModel = (
            await self.get_isolated_symbol_details(isolated_symbol)
        )

        # We extract the precision requirements
        first_currency_details: CurrencyCreditModel = isolated_symbol_details.first_currency_credit
        # We are sure that currency_pair_details is not `None` here
        currency_pair_details: PairModel = (
            first_currency_details.pair  # type: ignore[assignment]
        )

        volume_precision: int = currency_pair_details.first_currency_precision
        price_precision: int = currency_pair_details.price_precision
        self._logger.debug(
            "Precision values for [%s]: Volume -> [%s] | Price -> [%s]",
            isolated_symbol,
            volume_precision,
            price_precision,
        )

        return volume_precision, price_precision

    async def is_margin_asset_trade_able(self, isolated_symbol: str) -> bool:
        """Gets the trade-able status of requested margin asset from server.

        Returns the status as boolean. If the asset is not found or not active for margin trading,
        returns False instead of raising an exception.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset

        Returns:
            bool: Is margin asset trade-able?
        """
        self._logger.debug(
            "Trying to get trade-able status for [%s]",
            isolated_symbol,
        )

        # We try to get the data from server
        try:
            isolated_symbol_details: IsolatedSymbolDetailsModel = (
                await self.get_isolated_symbol_details(isolated_symbol)
            )

            # We extract the required variables
            asset_borrow_able: bool = isolated_symbol_details.borrow_active
            asset_transfer_able: bool = isolated_symbol_details.transfer_active
            asset_trade_able: bool = isolated_symbol_details.active
            asset_margin_active: bool = isolated_symbol_details.margin_active

            self._logger.debug(
                "Margin asset [%s] status:\n"
                "Borrow-able -> [%s] | Transfer-able -> [%s] | Trade-able -> [%s] | "
                "Margin-Active -> [%s]",
                isolated_symbol,
                asset_borrow_able,
                asset_transfer_able,
                asset_trade_able,
                asset_margin_active,
            )

        # If market is not found or asset is not available for margin trading
        # We catch the exception and return false
        except (MarketNotFoundError, MarginTradingNotActiveError):
            self._logger.exception(
                "Market not found or asset is not active for margin trading!\nCheck logs",
            )
            return False

        # If everything checks, we return the result
        return (
            asset_borrow_able and asset_transfer_able and asset_trade_able and asset_margin_active
        )

    async def open_margin_order(self, order: MarginOrderModel) -> int:
        """Opens a margin order.

        Args:
            order (MarginOrderModel): margin order object containing order details

        Raises:
            TypeError: If the server response is not a dictionary or does not indicate success.

        Returns:
            int: Order ID of the opened order
        """
        self._logger.debug(
            "Trying to open margin order for [%s]\nPrice: [%s] - Amount: [%s] - Direction: [%s]",
            order.isolated_symbol,
            order.order_price,
            order.deposit_amount,
            order.order_side.name,
        )

        # First we set the decimal context settings
        # Get the decimal context
        decimal_context: Context = getcontext()
        # Set Precision
        decimal_context.prec = DECIMAL_PRECISION
        # Set rounding method
        decimal_context.rounding = ROUND_DOWN
        # Set decimal context
        setcontext(decimal_context)

        # We calculate the variables
        # If the order is SELL, one level of margin is used for conversion by Tabdeal
        # so we have to step-down the margin level by one and calculate based on that
        if order.order_side is OrderSide.SELL:
            order.margin_level -= Decimal(1)
        self._logger.debug(
            "Order is [%s], margin level set to [%s]",
            order.order_side.name,
            order.margin_level,
        )

        # Next, we calculate the total USDT available for trading
        # and the amount of borrowed from Tabdeal based on margin level
        total_usdt_amount: Decimal = calculate_usdt(
            variable_one=order.deposit_amount,
            variable_two=order.margin_level,
            operation=MathOperation.MULTIPLY,
        )
        borrowed_usdt: Decimal = calculate_usdt(
            variable_one=total_usdt_amount,
            variable_two=order.deposit_amount,
            operation=MathOperation.SUBTRACT,
        )

        self._logger.debug(
            "Total USDT amount: [%s] - Borrowed USDT: [%s]",
            total_usdt_amount,
            borrowed_usdt,
        )

        # We calculate the volume of asset that we can buy with our money
        order_volume: Decimal = calculate_order_volume(
            asset_balance=total_usdt_amount,
            order_price=order.order_price,
            volume_fraction_allowed=order.volume_fraction_allowed,
            required_precision=order.volume_precision,
            order_side=order.order_side,
        )

        borrowed_volume: Decimal = calculate_order_volume(
            asset_balance=borrowed_usdt,
            order_price=order.order_price,
            volume_fraction_allowed=order.volume_fraction_allowed,
            required_precision=order.volume_precision,
            order_side=order.order_side,
        )

        self._logger.debug(
            "Order volume: [%s] - Borrowed volume: [%s]",
            order_volume,
            borrowed_volume,
        )

        # If the trade is BUY, the borrow quantity is based on USDT
        # Else, the borrow quantity is based on the asset and it's all of the order volume
        borrow_quantity: str = (
            str(
                borrowed_usdt,
            )
            if order.order_side is OrderSide.BUY
            else str(order_volume)
        )
        self._logger.debug(
            "Order is [%s]. Borrow quantity set to [%s]",
            order.order_side.name,
            borrow_quantity,
        )

        # We create the request data for sending to server
        margin_pair_id: int = await self.get_margin_pair_id(order.isolated_symbol)
        margin_order_data: str = json.dumps(
            obj={
                "market_id": (margin_pair_id),
                "side_id": str(order.order_side.value),
                "order_type_id": 1,
                "amount": str(order_volume),
                "borrow_amount": (borrow_quantity),
                "market_type": 3,
                "price": str(order.order_price),
            },
            default=str,  # To handle Decimal serialization
        )

        # Then, we send the request to the server
        server_response: dict[str, Any] | list[dict[str, Any]] = await self._post_data_to_server(
            connection_url=OPEN_MARGIN_ORDER_URI,
            data=margin_order_data,
        )

        # If the type is correct,
        # We check if the order was successful
        if (
            isinstance(server_response, dict)
            and server_response.get("message") == ORDER_PLACED_SUCCESSFULLY_RESPONSE
        ):
            # If the order is successful, we log and return order ID
            order_details: dict[str, Any] = server_response["order"]
            self._logger.debug(
                "Order placed successfully!\nOrder ID: [%s]\nOrder State: [%s]",
                order_details["id"],
                OrderState(order_details["state"]).name,
            )
            order_id: int = order_details["id"]
            return order_id

        # Else, we log and raise TypeError
        self._logger.error(
            "Expected dictionary, got [%s]",
            type(server_response),
        )

        raise TypeError

    async def set_sl_tp_for_margin_order(
        self,
        *,
        margin_asset_id: int,
        stop_loss_price: Decimal,
        take_profit_price: Decimal,
    ) -> None:
        """Sets the stop loss and take profit points.

        Args:
            margin_asset_id (int): Margin Asset ID (7 digits or more)
            stop_loss_price (Decimal): Stop loss price
            take_profit_price (Decimal): Take profit price

        Returns:
            None
        """
        self._logger.debug(
            "Trying to set SL [%s] and TP [%s] for margin asset with ID [%s]",
            stop_loss_price,
            take_profit_price,
            margin_asset_id,
        )

        # We create the request data to send to server
        data: str = json.dumps(
            obj={
                "trader_isolated_margin_id": margin_asset_id,
                "sl_price": str(stop_loss_price),
                "tp_price": str(take_profit_price),
            },
            default=str,  # To handle Decimal serialization
        )

        # We send the data to server
        _: dict[str, Any] | list[dict[str, Any]] = await self._post_data_to_server(
            connection_url=SET_SL_TP_FOR_MARGIN_ORDER_URI,
            data=data,
        )

        # If we reach here, then the request was successful
        self._logger.debug(
            "Stop loss [%s] and take profit [%s] has been set for margin asset with ID [%s]",
            stop_loss_price,
            take_profit_price,
            margin_asset_id,
        )

    async def does_margin_asset_have_active_order(self, isolated_symbol: str) -> bool:
        """Checks whether the margin asset has an active order or not.

        Args:
            isolated_symbol (str): Isolated symbol of margin asset

        Returns:
            bool: True if there is an active order, else False
        """
        self._logger.debug(
            "Checking if [%s] has active margin order",
            isolated_symbol,
        )
        # First, get all margin open orders
        all_active_margin_orders: list[
            MarginOpenOrderModel
        ] = await self.get_margin_all_open_orders()

        # If empty, return False
        if len(all_active_margin_orders) == 0:  # pragma: no cover
            return False

        # If has members, Get the input isolated_symbol margin asset ID
        margin_asset_id: int = await self.get_margin_asset_id(isolated_symbol=isolated_symbol)

        # Search the list to see whether an order with this ID is present
        # Get the first object in a list that meets a condition, if nothing found, return [None]
        margin_order: MarginOpenOrderModel | None = None
        for order in all_active_margin_orders:  # pragma: no cover
            if order.id == margin_asset_id:
                margin_order = order
                break

        # If present, return True, else return False
        return margin_order is not None

    async def is_margin_order_filled(self, isolated_symbol: str) -> bool:
        """Checks whether the isolated symbol's order is filled or not.

        Args:
            isolated_symbol (str): Isolated margin symbol

        Raises:
            MarginOrderNotFoundInActiveOrdersError: If the order is not found, we raise an exception

        Returns:
            bool: Is margin order filled?
        """
        self._logger.debug(
            "Checking whether order of margin asset [%s] is filled or not",
            isolated_symbol,
        )

        # First, get all margin open orders
        all_active_margin_orders: list[
            MarginOpenOrderModel
        ] = await self.get_margin_all_open_orders()

        # Get the input isolated_symbol margin asset ID
        margin_asset_id: int = await self.get_margin_asset_id(isolated_symbol=isolated_symbol)

        # Search the list for the matching order
        # Get the first object in a list that meets a condition, if nothing found, return [None]
        margin_order: MarginOpenOrderModel | None = None
        for order in all_active_margin_orders:
            if order.id == margin_asset_id:
                margin_order = order
                break

        # If none found, raise exception (Order not found in active orders!)
        if margin_order is None:
            raise MarginOrderNotFoundInActiveOrdersError

        # If found, return the state
        is_order_filled: bool = margin_order.is_order_filled
        return is_order_filled
