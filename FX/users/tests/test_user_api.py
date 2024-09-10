from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from ..serializers import UserSerializer

CREATE_USER_URL = reverse("user:create")
ME_URL = reverse("user:me")
GET_TOKEN_URL = reverse("user:token_obtain_pair")
REFRESH_TOKEN_URL = reverse("user:token_refresh")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicTransactionsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "Test Name",
            "username": "testusername",
            "trader_id": "13456",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "first_name": "Test",
            "last_name": "Test Name",
            "username": "testusername",
            "trader_id": "13456",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "Test Name",
            "username": "testusername",
            "trader_id": "13456",
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(GET_TOKEN_URL, payload)

        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_token_for_user(self):
        """Test refresh access token for valid credentials."""
        user_details = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "Test Name",
            "username": "testusername",
            "trader_id": "13456",
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(GET_TOKEN_URL, payload)
        payload = {"refresh": res.data["refresh"]}
        res = self.client.post(REFRESH_TOKEN_URL, payload)

        self.assertIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email="test@example.com", password="goodpass")
        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(GET_TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(GET_TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token_invalid_payload(self):
        """Test refreshing access token with invalid refresh token"""
        user_details = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "Test Name",
            "username": "testusername",
            "trader_id": "13456",
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(GET_TOKEN_URL, payload)
        payload = {"refresh": "some-random-token"}
        res = self.client.post(REFRESH_TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_empty_payload(self):
        """Test refreshing access token with empty refresh token"""
        user_details = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "Test Name",
            "username": "testusername",
            "trader_id": "13456",
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(GET_TOKEN_URL, payload)
        payload = {"refresh": ""}
        res = self.client.post(REFRESH_TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_required(self):
        """Test auth is requited for retrieving users."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        user_details = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "Test Name",
            "username": "testusername",
            "trader_id": "13456",
        }
        self.user = create_user(**user_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, UserSerializer(self.user).data)

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {"first_name": "Updated name", "password": "newpassword123"}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_user_profile_read_only_fields(self):
        """Test updating the user profile for the authenticated user."""
        profile_data = UserSerializer(self.user).data
        payload = {
            "is_active": False,
            "is_staff": True,
            "date_joined": timezone.now(),
            "email_verified": True,
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        new_profile_data = UserSerializer(self.user).data
        self.assertEqual(profile_data, new_profile_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_me_not_allowed(self):
        """Test DELETE is not allowed for the me endpoint"""
        res = self.client.delete(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
