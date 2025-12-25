from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        super_user = CustomUser(email="admin@admin.com", password="12345")
        super_user.username = "admin"
        super_user.set_password(super_user.password)
        super_user.is_staff = True
        super_user.is_active = True
        super_user.is_superuser = True
        super_user.save()
