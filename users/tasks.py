from celery import shared_task
from django.utils import timezone

from users.models import CustomUser


@shared_task
def check_last_login() -> None:
    users = CustomUser.objects.filter(is_active=True)

    for user in users:
        last_login = user.last_login.date() if user.last_login else None

        if last_login:
            if (timezone.now().today().date() - last_login).days > 5:
                user.is_active = False
                user.save()
                print(user.email)
