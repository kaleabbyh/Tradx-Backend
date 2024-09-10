from django.urls import include, path
from rest_framework import routers
from wallet import views

router = routers.DefaultRouter()
router.register(r"wallets", views.WalletViewSet)
router.register(r"transactions", views.TransactionViewSet)

app_name = "wallet"

urlpatterns = [
    path("", include(router.urls)),
    path("wallets/<int:wallet_id>/deposite", views.deposite_to_wallet),
    path("wallets/<int:wallet_id>/withdraw", views.withdraw_from_wallet),
]
