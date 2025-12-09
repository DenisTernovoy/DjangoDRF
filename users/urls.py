from rest_framework import routers
from django.urls import path
from users.views import CustomUserViewSet, PaymentListAPIView

app_name = "users"
user_router = routers.DefaultRouter()
user_router.register(r"users", CustomUserViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
]

urlpatterns += user_router.urls
