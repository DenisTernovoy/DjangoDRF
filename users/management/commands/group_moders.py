from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        Group.objects.all().delete()
        moders = Group.objects.create(name="moders")
        moders.save()
