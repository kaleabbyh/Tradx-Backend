from rest_framework.decorators import api_view, schema
from rest_framework.response import Response

from ..scripts.alpaca_integration import AlpacaIntegrationPositions


@api_view(["GET"])
@schema(None)
def get_positions(request):

    result = AlpacaIntegrationPositions().get_positions()

    return Response(result)
