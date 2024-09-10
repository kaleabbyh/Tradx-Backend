from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from ..views.alpaca_historical import get_crypto_bars


class AlpacaHistoricalTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_crypto_bars(self):
        pass
        request = self.factory.get("/api/alpaca/")
        response = get_crypto_bars(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions to validate the response data if needed
