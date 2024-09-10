from rest_framework.decorators import api_view, schema
from rest_framework.response import Response

from ..scripts.alpaca_integration import AlpacaIntegrationAssets


@api_view(["GET"])
@schema(None)
def get_assets(request):

    result = AlpacaIntegrationAssets().get_assets()

    return Response(result)
