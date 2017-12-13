import urllib
from datetime import datetime, timedelta
from random import randint

import os
from django.contrib.staticfiles.storage import staticfiles_storage as storage
import requests
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management import BaseCommand

from restaurants.models import Restaurant, CHOICES_RESTAURANT_TYPE, CHOICES_PRICE, CHOICES_TIME, ReservationInfo, \
    Comment, STAR_RATING

User = get_user_model()
user = User.objects.first()

base_location = storage.base_location
location = '/testimage/test1.png'
full_location = base_location + location
image = open(full_location, 'r')


img = File(open(os.path.join(storage.base_location + '/testimage/test1.png'), 'rb'))



class Command(BaseCommand):
    def handle(self, *args, **options):
        if Restaurant.objects.all().count() < 50:
            for i in range(11):
                restaurant = Restaurant(
                    name='Dummy Restaurant' + str(i),
                    address='패스트캠퍼스',
                    district='강남구',
                    geolocation='37.5499689,127.0234623',
                    contact_number='0200000000',
                    description='Dummy Restaurant description',
                    restaurant_type=CHOICES_RESTAURANT_TYPE[randint(0, len(CHOICES_RESTAURANT_TYPE) - 1)][0],
                    average_price=CHOICES_PRICE[randint(0, len(CHOICES_PRICE) - 1)][0],
                    business_hours='Dummy Business hour',
                    maximum_party=randint(1, 100),
                    owner=user,
                )
                restaurant.thumbnail.save('testimage.png', img)
                restaurant.menu.save('testimage.png', img)
                restaurant.save()
                for i in range(14):
                    for j in range(13):
                        if not ReservationInfo.objects.filter(restaurant=restaurant, time=CHOICES_TIME[j][0],
                                                              date=datetime.today() + timedelta(days=i)).count():
                            ReservationInfo.objects.create(
                                restaurant=restaurant,
                                time=CHOICES_TIME[j][0],
                                date=datetime.today() + timedelta(days=i)
                            )
                for i in range(1, 7):
                    Comment.objects.create(
                        author=user,
                        restaurant=Restaurant.objects.first(),
                        star_rate=STAR_RATING[randint(1, len(STAR_RATING) - 1)][0],
                        comment=f'Test Comment {i}'
                    )
            print("Successfully create dummy restaurants")
        else:
            print("Dummy Restaurant is over than 100")
