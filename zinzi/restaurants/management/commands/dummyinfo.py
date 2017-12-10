from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from restaurants.models import Restaurant, ReservationInfo, CHOICES_TIME

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        restaurant = Restaurant.objects.first()
        for i in range(14):
            for j in range(13):
                ReservationInfo.objects.create(
                    restaurant=restaurant,
                    time=CHOICES_TIME[j][0],
                    date=datetime.today() + timedelta(days=i)
                )
        print("Successfully create dummy info")
