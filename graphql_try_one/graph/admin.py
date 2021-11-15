from django.contrib import admin

from .models import TestModel, Order

admin.site.register(TestModel)
admin.site.register(Order)
