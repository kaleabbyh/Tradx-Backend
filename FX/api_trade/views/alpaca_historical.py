from rest_framework.decorators import api_view, schema
from rest_framework.response import Response

from ..scripts.alpaca_integration import AlpacaIntegrationDataHistorical


@api_view(["GET"])
@schema(None)
def get_crypto_bars(request):
    result = AlpacaIntegrationDataHistorical().get_crypto_bars()

    return Response(result)
