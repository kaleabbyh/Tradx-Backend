from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import AccountType, Transaction, Wallet
from ..serializers import TransactionSerializer

TRANSACTIONS_URL = "/api/wallet/transactions/"


def create_user(email="user@example.come", password="testpass123"):
    """Create and return user."""
    return get_user_model().objects.create_user(email=email, password=password)


def create_account_type(name="USD", is_fiat=False, is_active=True):
    """Create and return user."""
    return AccountType.objects.create(name=name, is_fiat=is_fiat, is_active=is_active)


def create_transaction(
    wallet,
    type="DEPOSIT",
    amount=100,
    currency="USD",
    status="PENDING",
    gateway_ref="traking-id-1234",
):
    """Create and return transaction."""
    return Transaction.objects.create(
        wallet=wallet,
        type=type,
        amount=amount,
        currency=currency,
        status=status,
        gateway_ref=gateway_ref,
    )


def detail_url(id):
    return f"{TRANSACTIONS_URL}{id}/"


class PublicTransactionsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is requited for retrieving transactions."""
        res = self.client.get(TRANSACTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTransactionsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.account_type = create_account_type()
        self.wallet = Wallet.objects.create(user=self.user, account_type=self.account_type)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_transactions(self):
        """Test retrieving a list of transactions."""
        create_transaction(self.wallet)
        res = self.client.get(TRANSACTIONS_URL)

        transactions = Transaction.objects.all().order_by("-created_at")
        serializer = TransactionSerializer(transactions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_transactions_limited_to_user(self):
        """Test list of transactions is limited to authenticated user."""
        user2 = create_user(email="user2@example.com")
        user2_wallet = Wallet.objects.create(user=user2, account_type=self.account_type)

        transaction_1 = create_transaction(self.wallet)
        create_transaction(user2_wallet)

        res = self.client.get(TRANSACTIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["wallet"], self.wallet.id)
        self.assertEqual(res.data[0]["id"], transaction_1.id)

    def test_get_transaction_details(self):
        """Test retrieving a transaction details."""
        transaction = create_transaction(self.wallet)

        url = detail_url(transaction.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["wallet"], self.wallet.id)
        self.assertEqual(res.data["id"], transaction.id)

    def test_get_other_users_transaction_details_fails(self):
        """Test retrieving a wallet details."""
        user2 = create_user(email="user2@example.com")
        user2_wallet = Wallet.objects.create(user=user2, account_type=self.account_type)
        transaction2 = create_transaction(user2_wallet)

        url = detail_url(transaction2.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_transaction_not_permitetd(self):
        """Test creating a transaction is not allowed."""
        payload = {}
        res = self.client.post(TRANSACTIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_transaction_not_permitetd(self):
        """Test updating an transaction is not allowed."""
        transaction = create_transaction(self.wallet)
        payload = {}
        url = detail_url(transaction.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_transaction_not_permitted(self):
        """Test deleting a transaction is not allowed."""
        transaction = create_transaction(self.wallet)
        url = detail_url(transaction.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
