from django.contrib import admin

from .models import TestModel, Order, Item, Region, DeliveryModel, Shipment


admin.site.register(TestModel)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Region)
admin.site.register(DeliveryModel)
admin.site.register(Shipment)
