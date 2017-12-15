from random import randint

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APILiveServerTestCase

from restaurants.models import Restaurant
from restaurants.views import RestaurantListView

User = get_user_model()

#
# class RestaurantListViewTest(APILiveServerTestCase):
#     URL_RESTAURANT_LIST_NAME = 'restaurants:restaurant-list'
#     URL_RESTAURANT_LIST = '/restaurants/'
#     VIEW_CLASS = RestaurantListView
#
#     @staticmethod
#     def create_user(email='test@test.test', name='dummy'):
#         return User.objects.create_user(email=email, name=name)
#
#     @staticmethod
#     def create_restaurant(email='test@test.test', name='dummy'):
#         user = User.objects.create_user(email=email, name=name)
#         return Restaurant.objects.create(
#             name='Dummy Restaurant',
#             address='패스트캠퍼스',
#             district='강남구',
#             geolocation='37.5499689,127.0234623',
#             contact_number='0200000000',
#             description='Dummy Restaurant description',
#             restaurant_type='kor',
#             average_price='c',
#             business_hours='Dummy Business hour',
#             maximum_party=randint(1, 100),
#             owner=user,
#         )
#
#     def test_restaurant_list_url_name_reverse(self):
#         url = reverse(self.URL_RESTAURANT_LIST_NAME)
#         self.assertEqual(url, self.URL_RESTAURANT_LIST)
