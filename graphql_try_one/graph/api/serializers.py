from rest_framework.serializers import ModelSerializer

from graph.models import Order


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 3
