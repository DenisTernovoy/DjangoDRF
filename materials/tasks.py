from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from materials.models import Course
from materials.services import get_recipient_list


@shared_task
def send_information_about_course(email_list: list) -> None:
    """Отправляет сообщение подписчику обновленного курса"""

    send_mail(
        subject="Обновление курса",
        message="Произошло обновление курса, на который Вы подписаны!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email_list,
    )


@shared_task
def send_email_notice(course_pk: Course) -> None:
    """Отправляет сообщение подписчику обновленного курса"""

    course = Course.objects.get(pk=course_pk)
    today = timezone.now()
    difference = today - course.last_update
    minutes = difference.seconds // 60

    if minutes >= 60 * 4:

        # Получение списка email-адресов подписчиков
        email_list = get_recipient_list(course_pk)

        send_mail(
            subject="Обновление курса",
            message="Произошло обновление урока внутри курса, на который Вы подписаны!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list,
        )

        # Обновление времени последнего изменения
        course.last_update = timezone.now()
        course.save()

    pass
