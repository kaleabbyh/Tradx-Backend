from uuid import UUID

from api_trade.serializers import OrderSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..scripts.alpaca_integration import AlpacaIntegrationOrders


class AlpacaOrdersViewSet(viewsets.ViewSet):
    """
    ViewSet to handle Alpaca orders.
    """

    serializer_class = OrderSerializer

    def list(self, request):
        """
        Return a list of all orders.
        """
        result = AlpacaIntegrationOrders().get_orders()
        return Response(result)

    def create(self, request):
        """
        Create a new order.
        """
        # print(request.data)
        result = AlpacaIntegrationOrders().place_order(request.data)
        return Response(result)

    def retrieve(self, request, order_id: UUID = None):
        """
        Retrieve a specific order by ID.
        """
        try:
            result = AlpacaIntegrationOrders().get_order(order_id=order_id)
            return Response(result)
        except ValueError as e:
            return Response({"error": f"{e}"}, status=400)

    def destroy(self, request, order_id: UUID = None):
        """
        Delete an order by id.
        """
        try:
            result = AlpacaIntegrationOrders().cancel_order(order_id)
            return Response(result, status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({"error": f"{e}"}, status=400)

    @action(detail=False, methods=["delete"])
    def cancel_all(self, request):
        """
        Cancel all orders.
        """
        result = AlpacaIntegrationOrders().cancel_all_orders()
        return Response(result)
