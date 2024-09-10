from rest_framework.decorators import api_view, schema
from rest_framework.response import Response

from ..scripts.alpaca_integration import AlpacaIntegrationAccount


@api_view(["GET"])
@schema(None)
def get_view_gain_loss_portfolio(request):

    result = AlpacaIntegrationAccount().get_view_gain_loss_portfolio()

    return Response(result)
