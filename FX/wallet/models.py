from django.db import models

# Create your models here.
from users.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountType(TimeStampedModel):
    name = models.CharField(max_length=5)
    is_fiat = models.BooleanField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.name


class Wallet(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    account_type = models.ForeignKey(AccountType, on_delete=models.RESTRICT)
    balance = models.FloatField(default=0.0)
    available_balance = models.FloatField(default=0.0)

    class Meta:
        unique_together = ["user", "account_type"]

    def __str__(self):
        return f"{self.user}-{self.account_type}"


class Transaction(TimeStampedModel):
    TYPE_CHOICES = (
        ("D", "DEPOSIT"),
        ("W", "WITHDRAWAL"),
        ("TD", "TRADE"),
        ("TN", "TRANSFER"),
    )
    STATUS_CHOICES = (
        ("P", "PENDING"),
        ("S", "SUCCESSFUL"),
        ("F", "FAILED"),
        ("R", "REFUNDED"),
    )
    wallet = models.ForeignKey(Wallet, on_delete=models.RESTRICT)
    type = models.CharField(choices=TYPE_CHOICES)
    amount = models.FloatField()
    currency = models.CharField(max_length=5)
    status = models.CharField(choices=STATUS_CHOICES)
    gateway_ref = models.CharField(max_length=255)
