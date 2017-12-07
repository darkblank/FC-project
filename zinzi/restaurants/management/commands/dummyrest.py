import os
from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from restaurants.models import Restaurant, CHOICES_RESTAURANT_TYPE, CHOICES_PRICE

User = get_user_model()

path = list()
for i in range(1, 5):
    path += os.path.join(settings.STATIC_DIR, 'testimage', 'test' + str(i) + '.png')


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Restaurant.objects.all().count() < 500:
            for i in range(500):
                Restaurant.objects.create(
                    name='Dummy Restaurant' + str(i),
                    address='Dummy address' + str(i),
                    geolocation='37.5499689,127.0234623',
                    contact_number='0200000000',
                    description='Dummy Restaurant description',
                    restaurant_type=CHOICES_RESTAURANT_TYPE[randint(0, len(CHOICES_RESTAURANT_TYPE) - 1)][0],
                    average_price=CHOICES_PRICE[randint(0, len(CHOICES_PRICE) - 1)][0],
                    thumbnail=path[randint(0, 4)],
                    menu=path[randint(0, 4)],
                    business_hours='Dummy Business hour',
                    maximum_party=randint(1, 100),
                    owner=User.objects.first(),
                )
            print("Successfully create dummy restaurants")
        else:
            print("Dummy Restaurant is over than 100")
