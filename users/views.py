from django.db.models import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser, Payment
from users.permissions import IsUser
from users.serializers import (
    CustomUserPaymentSerializer,
    CustomUserSerializer,
    CustomUserSerializerAny,
    PaymentSerializer,
)
from users.services import (
    check_stripe_status,
    create_stripe_price,
    create_stripe_session,
)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action in ("destroy", "update", "partial_update"):
            permission_classes = [IsAuthenticated, IsUser]
        else:
            permission_classes = []

        return [p() for p in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.id != instance.id:
            serializer = CustomUserSerializerAny(instance)
        else:
            serializer = CustomUserPaymentSerializer(instance)

        return Response(serializer.data)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "pay_type"]
    ordering_fields = [
        "pay_date",
    ]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создает объект модели платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.course:
            payment.pay_amount = payment.course.amount
        else:
            payment.pay_amount = payment.lesson.amount
        payment.save()


class PaymentAPIView(APIView):
    """Создание оплаты курса или урока"""

    queryset = Payment.objects.all()

    def post(self, *args, **kwargs):
        data = self.request.data

        try:
            payment = Payment.objects.get(pk=data["payment"])
        except ObjectDoesNotExist:
            return Response("Платежа с таким id не существует")

        price = create_stripe_price(
            payment.pay_amount, payment.course if payment.course else payment.lesson
        )
        payment_url, payment_id = create_stripe_session(price["id"])

        payment.session_id = payment_id
        payment.save()

        return Response({"pay_url": payment_url})


@api_view(["GET"])
def check_status_payment(request):

    try:
        payment = Payment.objects.get(pk=request.data["payment"])
    except ObjectDoesNotExist:
        return Response("Платежа с таким id не существует")

    result = check_stripe_status(payment.session_id)
    payment.status = result
    payment.save()

    return Response(result)
