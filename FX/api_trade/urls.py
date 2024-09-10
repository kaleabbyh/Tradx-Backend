from api_trade.views import (
    alpaca_account_view,
    alpaca_assets_view,
    alpaca_historical,
    alpaca_order_view,
    alpaca_position_view,
)
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()


app_name = "api_trade"

urlpatterns = [
    path("alpaca/", alpaca_historical.get_crypto_bars, name="historical-data"),
    path("alpaca/assets/", alpaca_assets_view.get_assets, name="assets"),
    path(
        "alpaca/orders/",
        alpaca_order_view.AlpacaOrdersViewSet.as_view({"get": "list", "post": "create", "delete": "cancel_all"}),
        name="orders",
    ),
    path(
        "alpaca/orders/detail/<str:order_id>/",
        alpaca_order_view.AlpacaOrdersViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="orders-detail",
    ),
    path("alpaca/positions/", alpaca_position_view.get_positions, name="positions"),
    path(
        "alpaca/accounts/",
        alpaca_account_view.get_view_gain_loss_portfolio,
        name="accounts",
    ),
]
