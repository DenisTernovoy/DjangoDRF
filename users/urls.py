from rest_framework import routers
from users.views import (
    CustomUserViewSet,
    PaymentListAPIView,
    PaymentAPIView,
    PaymentCreateAPIView,
)
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users"
user_router = routers.DefaultRouter()
user_router.register(r"users", CustomUserViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("pay/", PaymentAPIView.as_view(), name="payment-pay"),
]

urlpatterns += user_router.urls
