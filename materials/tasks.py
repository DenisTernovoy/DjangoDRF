from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_information_about_course(email_list: list) -> None:
    send_mail(
        subject="Обновление курса",
        message="Произошло обновление курса, на который Вы подписаны!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email_list,
    )
