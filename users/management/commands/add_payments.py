from datetime import datetime

from django.core.management.base import BaseCommand
from users.models import Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        Payment.objects.all().delete()

        Payment.objects.create(
            user_id=2,
            pay_date=datetime.now(),
            lesson_id=1,
            pay_amount=1000,
            pay_type="cash",
        )

        Payment.objects.create(
            user_id=2,
            pay_date=datetime.now(),
            course_id=1,
            pay_amount=10000,
            pay_type="cash",
        )
