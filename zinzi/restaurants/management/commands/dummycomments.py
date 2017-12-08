from random import randint

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from restaurants.models import Restaurant, Comment, STAR_RATING

User = get_user_model()
user = User.objects.first()


class Command(BaseCommand):
    def handle(self, *args, **options):
        for rest in Restaurant.objects.all():
            for i in range(1, 7):
                Comment.objects.create(
                    author=user,
                    restaurant=rest,
                    star_rate=STAR_RATING[randint(1, len(STAR_RATING) - 1)][0],
                    comment=f'Test Comment {rest.pk}'
                )
        print("Successfully create dummy Comments")
