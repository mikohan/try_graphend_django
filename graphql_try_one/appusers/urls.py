from django.urls import path

from appusers.views import UserCreateAPIView


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", UserCreateAPIView.as_view(), name="register"),
]
