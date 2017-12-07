from datetime import datetime
from random import randint

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from restaurants.models import Restaurant, ReservationInfo, CHOICES_TIME

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        restaurant = Restaurant.objects.first()
        for i in range(13):
            ReservationInfo.objects.create(
                restaurant=restaurant,
                time=CHOICES_TIME[i-1][0],
                date=datetime.today()
            )
        print("Successfully create dummy infos")
