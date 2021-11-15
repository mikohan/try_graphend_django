from rest_framework.serializers import ModelSerializer

from graph.models import Delivery, Order


class DeliverySerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["id", "name", "region", "shipments"]


class OrderSerializer(ModelSerializer):
    # delivery = DeliverySerializer

    class Meta:
        model = Order
        fields = [
            "id",
            "currency",
            "delivery",
        ]
        depth = 3
