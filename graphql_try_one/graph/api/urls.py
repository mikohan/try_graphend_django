from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from .views import OrderUpdateStatusAPI, OrderViewSetAPI
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"order", OrderViewSetAPI, basename="order")

urlpatterns = [
    path("", include(router.urls)),
    path("status/", OrderUpdateStatusAPI.as_view(), name="update"),
]
