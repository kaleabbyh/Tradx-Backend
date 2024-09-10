from rest_framework import serializers


# Serializer
class CryptoBarsSerializer(serializers.Serializer):
    symbol = serializers.CharField(required=True)
    timeframe = serializers.CharField()
    start = serializers.DateField()


class OrderSerializer(serializers.Serializer):
    """Order serializer.

    Attributes:
    symbol (str): The symbol identifier for the asset being traded
    qty (Optional[float]): The number of shares to trade. Fractional qty for stocks only with market orders.
    notional (Optional[float]): The base currency value of the shares to trade. For stocks, only works with MarketOrders.
        **Does not work with qty**.
    side (OrderSide): Whether the order will buy or sell the asset.
    type (OrderType): The execution logic type of the order (market, limit, etc).
    time_in_force (TimeInForce): The expiration logic of the order.
    extended_hours (Optional[float]): Whether the order can be executed during regular market hours.
    client_order_id (Optional[str]): A string to identify which client submitted the order.
    order_class (Optional[OrderClass]): The class of the order. Simple orders have no other legs.
    take_profit (Optional[TakeProfitRequest]): For orders with multiple legs, an order to exit a profitable trade.
    stop_loss (Optional[StopLossRequest]): For orders with multiple legs, an order to exit a losing trade.
    """  # noqa

    symbol = serializers.CharField(required=True, max_length=25)
    qty = serializers.FloatField(required=False)
    side = serializers.ChoiceField(choices=["buy", "sell"])
    notional = serializers.FloatField(required=False)
    type = serializers.ChoiceField(
        choices=[
            "market",
            "limit",
            "stop",
            "stop_limit",
            "trailing_stop",
        ],
        required=False,
    )
    time_in_force = serializers.ChoiceField(
        choices=[
            "day",
            "gtc",
            "opg",
            "ioc",
            "fok",
            "cls",
        ]
    )
    order_class = serializers.ChoiceField(
        choices=[
            "simple",
            "bracket",
            "oco",
            "oto",
        ],
        required=False,
    )
    extended_hours = serializers.FloatField(required=False)
    client_order_id = serializers.CharField(required=False, max_length=125)
    take_profit = serializers.FloatField(required=False)
    stop_loss = serializers.FloatField(required=False)
    limit_price = serializers.FloatField(required=False)


class OrderIdSerializer(serializers.Serializer):
    """Order ID serializer.

    Attributes:
    order_id (str): The unique identifier of the order.
    """

    order_id = serializers.CharField(required=True, max_length=25)
