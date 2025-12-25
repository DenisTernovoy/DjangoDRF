from materials.models import Subscription


def get_recipient_list(course_pk: int) -> list:
    """Возвращает список email-адресов всех подписчиков курса по его id"""

    subscriptions = Subscription.objects.filter(course=course_pk)
    user_list_email = []

    for sub in subscriptions:
        user_list_email.append(sub.subscriber.email)

    return user_list_email
