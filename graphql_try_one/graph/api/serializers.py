from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from graph.models import DeliveryModel, Item, Order, Region, Shipment


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ShipmentsSerializer(ModelSerializer):
    shipmentDate = serializers.DateField(input_formats=["%d-%m-%Y"])

    class Meta:
        model = Shipment
        fields = ["id", "shipmentDate"]


class RegionSerializer(ModelSerializer):
    type = serializers.CharField(source="regionT")
    parent = RecursiveField(required=False)

    class Meta:
        model = Region
        fields = ["id", "name", "type", "parent"]
        extra_kwargs = {
            "id": {"read_only": False},
            "id": {"validators": []},
        }


class DeliverySerializer(ModelSerializer):
    type = serializers.CharField(source="t_attention")
    shipments = ShipmentsSerializer(many=True)
    region_id = serializers.CharField(source="region", required=False)
    region = RegionSerializer()

    class Meta:
        model = DeliveryModel
        fields = ["region_id", "serviceName", "type", "shipments", "region"]


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id",
            "feedId",
            "offerId",
            "offerName",
            "price",
            "subsidy",
            "count",
            "delivery",
            "params",
            "vat",
            "fulfilmentShopId",
            "sku",
            "shopSku",
            "warehouseId",
            "partnerWarehouseId",
        ]
        extra_kwargs = {
            "id": {"read_only": False},
            "id": {"validators": []},
        }


class OrderSerializer(ModelSerializer):
    delivery = DeliverySerializer()
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "currency",
            "fake",
            "paymentType",
            "paymentMethod",
            "taxSystem",
            "delivery",
            "items",
        ]
        depth = 3

    def create(self, validated_data):
        delivery = validated_data.pop("delivery")
        shipments = delivery.pop("shipments")
        region = delivery.pop("region")
        items_data = validated_data.pop("items")

        try:
            region_object = Region.objects.get(id=region.get("id"))
        except:
            region_object = Region(
                id=region.get("id"),
                name=region.get("name"),
                regionT=region.get("type"),
            )
            region_object.save()

        order = Order(
            id=validated_data.get("id"),
            currency=validated_data["currency"],
            fake=validated_data["fake"],
            paymentType=validated_data["paymentType"],
            paymentMethod=validated_data["paymentMethod"],
            taxSystem=validated_data["taxSystem"],
        )
        order.save()
        # Delivery object here
        delivery_object = DeliveryModel(
            order=order,
            serviceName=delivery.get("serviceName"),
            t_attention=delivery.get("type"),
            region=region_object,
        )
        delivery_object.save()
        # Ship object working
        for ship in shipments:
            ship_obj = Shipment(
                delivery=delivery_object,
                id=ship["id"],
                shipmentDate=ship["shipmentDate"],
            )
            ship_obj.save()
        # Items ojects save
        for item in items_data:
            it = Item(
                order=order,
                id=item.get("id"),
                feedId=item.get("feedId"),
                offerId=item.get("offerId"),
                offerName=item.get("offerName"),
                price=item.get("price"),
                count=item.get("count"),
                delivery=item.get("delivery"),
                params=item.get("params"),
                vat=item.get("vat"),
                sku=item.get("sku"),
                fulfilmentShopId=item.get("fulfilmentShopId"),
                shopSku=item.get("shopSku"),
                warehouseId=item.get("werehouseId"),
                partnerWarehouseId=item.get("partnerWarehouseId"),
            )
            it.save()

        return order
