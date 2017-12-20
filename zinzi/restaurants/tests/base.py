from random import randint

from django.contrib.auth import get_user_model
from rest_framework.test import APILiveServerTestCase

from restaurants.models import CHOICES_PRICE, CHOICES_RESTAURANT_TYPE, Restaurant

User = get_user_model()


class RestaurantTestBase(APILiveServerTestCase):
    @staticmethod
    def create_user(email='test@test.test', name='dummy'):
        if User.objects.count():
            return User.objects.first()
        return User.objects.create_user(email=email, name=name)

    @staticmethod
    def create_user2(email='test2@test2.test2', name='dummy2'):
        if User.objects.count() < 2:
            return User.objects.create_user(email=email, name=name)
        return User.objects.last()

    @staticmethod
    def create_restaurant(user=None):
        if not user:
            user = RestaurantTestBase.create_user()
        return Restaurant.objects.create(
            name='Dummy Restaurant',
            address='패스트캠퍼스',
            geolocation='37.5499689,127.0234623',
            contact_number='0200000000',
            description='Dummy Restaurant description',
            restaurant_type=CHOICES_RESTAURANT_TYPE[randint(0, len(CHOICES_RESTAURANT_TYPE) - 1)][0],
            average_price=CHOICES_PRICE[randint(0, len(CHOICES_PRICE) - 1)][0],
            business_hours='Dummy Business hour',
            maximum_party=randint(1, 100),
            owner=user,
        )
