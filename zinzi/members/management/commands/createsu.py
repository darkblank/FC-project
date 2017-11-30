from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email=settings.SUPERUSER_EMAIL).exists():
            user = User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                nickname=settings.SUPERUSER_NICKNAME,
                phone_number=settings.SUPERUSER_PHONE,
                password=settings.SUPERUSER_PASSWORD,
            )
            print(f'Created superuser ({user.email})')
        else:
            print(f'Superuser already exists')
