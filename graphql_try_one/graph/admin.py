from django.contrib import admin

from .models import TestModel, Order, Item, Region, Delivery, Shipment


admin.site.register(TestModel)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Region)
admin.site.register(Delivery)
admin.site.register(Shipment)
