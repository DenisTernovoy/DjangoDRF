from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.validators import ValidationError

from materials.models import Course, Lesson


# Create your models here.
class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=20, verbose_name="Телефон", null=True, blank=True
    )
    city = models.CharField(max_length=30, verbose_name="Город", null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):

    TYPES_OF_PAY = [
        ("cash", "Наличные"),
        ("transaction", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
        null=True,
        blank=True,
    )
    pay_date = models.DateField(auto_now_add=True)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name="payments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True, related_name="payments"
    )
    pay_amount = models.IntegerField(null=True, blank=True)
    pay_type = models.CharField(
        choices=TYPES_OF_PAY, max_length=30, null=True, blank=True
    )
    status = models.CharField(
        max_length=25, default="open", verbose_name="Статус платежа"
    )
    session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID платежа в stripe"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user.email} - {self.pay_amount}"
