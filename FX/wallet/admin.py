from django.contrib import admin
from wallet.models import AccountType, Transaction, Wallet


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "is_fiat", "is_active"]
    search_fields = ["name"]

    class Meta:
        model = AccountType


admin.site.register(AccountType, AccountTypeAdmin)


class WalletAdmin(admin.ModelAdmin):
    list_display = ["user", "account_type", "balance", "available_balance"]
    search_fields = ["user"]
    list_filter = ["account_type"]

    class Meta:
        model = Wallet


admin.site.register(Wallet, WalletAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ["wallet", "type", "amount", "currency", "status"]
    list_filter = ["type", "currency", "status"]

    class Meta:
        model = Transaction


admin.site.register(Transaction, TransactionAdmin)
