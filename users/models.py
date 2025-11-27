from django.db import models
from django.contrib.auth.models import AbstractUser


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
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
