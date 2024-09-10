from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from wallet.models import Transaction, Wallet
from wallet.permissions import IsOwner
from wallet.serializers import TransactionSerializer, WalletSerializer


class WalletViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Fiter queryset to authenticated user."""
        queryset = self.queryset
        queryset = queryset.filter(user=self.request.user).order_by("-created_at")
        return queryset


class TransactionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Fiter queryset to authenticated user."""
        queryset = self.queryset
        queryset = queryset.filter(wallet__user=self.request.user).order_by("-created_at")
        return queryset


@api_view(["POST"])
def deposite_to_wallet(request, wallet_id):
    # Input Validations:
    try:
        wallet = Wallet.objects.get(id=wallet_id)
    except Wallet.DoesNotExist:
        response = {"detail": f"Wallet with id {wallet_id} doesn't exist"}
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    # Ensure wallet ID belongs to the authenticated user.
    if not wallet.user.id == request.user.id:
        response = {"detail": "You do not have permission to perform this action."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    # TODO:
    # Verify the deposit amount is greater than the minimum required.
    # (Optional) Check if any deposit limits are in place for the user.

    # Payment Gateway Integration:

    # Initiate a transaction with the selected payment gateway (Stripe, PayPal).
    # Pass the deposit amount and any metadata needed by the gateway.
    # Redirect the user to the gateway (if an external redirect flow is used) or get a
    # payment confirmation token (depending on the gateway method).

    # Transaction Creation:

    # Create a new record in Transactions table.
    # type: "DEPOSIT"
    # status: "PENDING"
    # gateway_ref: Token or relevant ID from the payment gateway.

    # Monitor Payment Gateway:

    # Webhook/Status Check: set up a webhook to receive an update about the transaction for the status.

    # Success:
    # Update the status in the Transactions table to "SUCCESSFUL".
    # Increment the wallet's balance (and available_balance) in the database.

    # Failure:
    # Update Transactions table status to "FAILED".
    # (Optional) Implement a refund mechanism depending on gateway functionality.

    return Response({})


@api_view(["POST"])
def withdraw_from_wallet(request, wallet_id):
    # Input Validations:
    try:
        wallet = Wallet.objects.get(id=wallet_id)
    except Wallet.DoesNotExist:
        response = {"detail": f"Wallet with id {wallet_id} doesn't exist"}
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    # Ensure wallet ID belongs to the authenticated user.
    if not wallet.user.id == request.user.id:
        response = {"detail": "You do not have permission to perform this action."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    # TODO:
    # Check if enough available_balance exists.
    # Verify withdrawal amount meets any minimum/maximum limits.

    # Payment Gateway Integration:

    # Initiate the withdrawal with the selected gateway.
    # Provide relevant destination information (e.g., bank account).

    # Transaction Creation:

    # Create an entry in Transactions table
    # type: "WITHDRAWAL"
    # status: "PENDING"
    # gateway_ref: Token or relevant ID from the payment gateway

    # Monitor & Update:  Similar monitoring logic as in the deposit flow for success/failure updates.

    return Response({})
