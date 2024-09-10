from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import AccountType, Wallet
from ..serializers import WalletSerializer

WALLETS_URL = "/api/wallet/wallets/"


def create_user(email="user@example.come", password="testpass123"):
    """Create and return user."""
    return get_user_model().objects.create_user(email=email, password=password)


def create_account_type(name="USD", is_fiat=False, is_active=True):
    """Create and return user."""
    return AccountType.objects.create(name=name, is_fiat=is_fiat, is_active=is_active)


def detail_url(id):
    return f"{WALLETS_URL}{id}/"


class PublicWalletsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is requited for retrieving wallets."""
        res = self.client.get(WALLETS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWalletsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.account_type = create_account_type()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_wallets(self):
        """Test retrieving a list of wallets."""
        Wallet.objects.create(user=self.user, account_type=self.account_type)

        res = self.client.get(WALLETS_URL)

        wallets = Wallet.objects.all().order_by("-created_at")
        serializer = WalletSerializer(wallets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_wallets_limited_to_user(self):
        """Test list of wallets is limited to authenticated user."""
        user2 = create_user(email="user2@example.com")
        Wallet.objects.create(user=user2, account_type=self.account_type)
        wallet = Wallet.objects.create(user=self.user, account_type=self.account_type)

        res = self.client.get(WALLETS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["user"], self.user.id)
        self.assertEqual(res.data[0]["id"], wallet.id)

    def test_get_wallet_details(self):
        """Test retrieving a wallet details."""
        wallet = Wallet.objects.create(user=self.user, account_type=self.account_type)

        url = detail_url(wallet.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["user"], self.user.id)
        self.assertEqual(res.data["id"], wallet.id)

    def test_get_other_users_wallet_details_fails(self):
        """Test retrieving a wallet details."""
        Wallet.objects.create(user=self.user, account_type=self.account_type)

        user2 = create_user(email="user2@example.com")
        wallet2 = Wallet.objects.create(user=user2, account_type=self.account_type)

        url = detail_url(wallet2.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_wallet(self):
        """Test creating a wallet."""
        payload = {"account_type": self.account_type.id}
        res = self.client.post(WALLETS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["user"], self.user.id)
        self.assertEqual(res.data["account_type"], self.account_type.id)

    def test_create_wallet_with_same_accunt_type_fails(self):
        """Test creating a wallet with same user and account type fails."""
        Wallet.objects.create(user=self.user, account_type=self.account_type)

        payload = {"account_type": self.account_type.id}
        res = self.client.post(WALLETS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wallet_inactive_account_type_fails(self):
        """Test creating a wallet with inactive account fails."""
        account_type = create_account_type(is_active=False)
        payload = {"account_type": account_type.id}
        res = self.client.post(WALLETS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_creation_with_read_only_fields(self):
        """Test creating a wallet with"""
        user2 = create_user(email="user2@gmail.com")
        payload = {"account_type": self.account_type.id, "balance": 100.0, "available_balance": 100.0, "user": user2.id}
        res = self.client.post(WALLETS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.data["balance"], 100)
        self.assertNotEqual(res.data["available_balance"], 100)
        self.assertNotEqual(res.data["user"], user2.id)
        self.assertEqual(res.data["balance"], 0.0)
        self.assertEqual(res.data["available_balance"], 0.0)
        self.assertEqual(res.data["user"], self.user.id)

    def test_update_wallet_not_permitetd(self):
        """Test updating an wallet."""
        wallet = Wallet.objects.create(user=self.user, account_type=self.account_type)
        payload = {}

        url = detail_url(wallet.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_wallet_not_permitted(self):
        """Test deleting a wallet."""
        wallet = Wallet.objects.create(user=self.user, account_type=self.account_type)

        url = detail_url(wallet.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
