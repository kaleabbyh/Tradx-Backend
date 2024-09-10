from django.db import IntegrityError
from rest_framework import serializers
from wallet.models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = (
            "user",
            "balance",
            "available_balance",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user

        # Restrict wallet creation if account_type is not active
        is_account_type_active = validated_data["account_type"].is_active
        if not is_account_type_active:
            raise serializers.ValidationError({"account_type": ["Account type is not active."]})

        # Ensure user can have only one account with each account_type.
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"non_field_errors": ["Wallet with this User and Account type already exists."]}
            )


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
        )
