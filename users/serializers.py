from rest_framework import serializers

from users.models import CustomUser, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


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
