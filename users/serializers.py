from rest_framework import serializers

from users.models import CustomUser, Payment
from users.validators import PaymentValidator


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        validators = [
            PaymentValidator("course", "lesson"),
        ]


class CustomUserPaymentSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "phone",
            "city",
            "payments",
        )


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserSerializerAny(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("email", "city")
