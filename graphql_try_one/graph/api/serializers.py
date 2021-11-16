from rest_framework.serializers import ModelSerializer

from graph.models import DeliveryModel, Order


class DeliverySerializer(ModelSerializer):
    class Meta:
        model = DeliveryModel
        fields = ["id", "name", "region", "shipments"]


class OrderSerializer(ModelSerializer):
    delivery = DeliverySerializer

    class Meta:
        model = Order
        fields = ["id", "currency", "delivery", "items"]
        depth = 1
