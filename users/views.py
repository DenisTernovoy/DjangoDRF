from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.response import Response

from users.models import CustomUser, Payment
from users.serializers import (
    CustomUserSerializer,
    PaymentSerializer,
    CustomUserPaymentSerializer,
)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CustomUserPaymentSerializer(instance)

        return Response(serializer.data)


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "pay_type"]
    ordering_fields = [
        "pay_date",
    ]
