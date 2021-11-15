from rest_framework.viewsets import ModelViewSet
from graph.models import Order
from .serializers import OrderSerializer


class OrderViewSetAPI(ModelViewSet):

    """
    Testing viewset for correct structure

    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
