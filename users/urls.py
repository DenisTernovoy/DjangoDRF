from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import (CustomUserViewSet, PaymentAPIView,
                         PaymentCreateAPIView, PaymentListAPIView,
                         check_status_payment)

app_name = "users"
user_router = routers.DefaultRouter()
user_router.register(r"users", CustomUserViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("pay/", PaymentAPIView.as_view(), name="payment-pay"),
    path("pay/check/", check_status_payment, name="payment-check"),
]

urlpatterns += user_router.urls
