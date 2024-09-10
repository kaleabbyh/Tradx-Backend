from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    trader_id = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="user_profile_pictures", blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    two_factor_authentication_enabled = models.BooleanField(default=False)
    hidden_account_balances_toggle_enabled = models.BooleanField(default=False)
    one_click_trade_toggle_enabled = models.BooleanField(default=False)
    one_click_trade_closing_toggle_enabled = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
