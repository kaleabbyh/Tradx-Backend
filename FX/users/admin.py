from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.forms import UserChangeForm, UserCreationForm
from users.models import User

admin.site.site_header = "FX Portal Administration"


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            None,
            {
                "fields": (
                    "trader_id",
                    "username",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "birthdate",
                    "profile_picture",
                    "address",
                    "gender",
                    "email_verified",
                    "two_factor_authentication_enabled",
                    "hidden_account_balances_toggle_enabled",
                    "one_click_trade_toggle_enabled",
                    "one_click_trade_closing_toggle_enabled",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            None,
            {
                "fields": (
                    "trader_id",
                    "username",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "birthdate",
                    "profile_picture",
                    "address",
                    "gender",
                    "email_verified",
                    "two_factor_authentication_enabled",
                    "hidden_account_balances_toggle_enabled",
                    "one_click_trade_toggle_enabled",
                    "one_click_trade_closing_toggle_enabled",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
