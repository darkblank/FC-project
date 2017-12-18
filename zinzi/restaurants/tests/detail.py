from random import randint

from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from restaurants.models import Restaurant, CHOICES_RESTAURANT_TYPE, CHOICES_PRICE
from restaurants.views import RestaurantDetailView

User = get_user_model()


class RestaurantDetailViewTest(APILiveServerTestCase):
    URL_RESTAURANT_DETAIL_NAME = 'restaurants:restaurant-detail'
    URL_RESTAURANT_DETAIL = '/restaurants/1/'
    VIEW_CLASS = RestaurantDetailView

    @staticmethod
    def create_user(email='test@test.test', name='dummy'):
        return User.objects.create_user(email=email, name=name)

    @staticmethod
    def create_restaurant(user=None):
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

    def test_restaurant_detail_url_name_reverse(self):
        url = reverse(self.URL_RESTAURANT_DETAIL_NAME, kwargs={'pk': 1})
        self.assertEqual(url, self.URL_RESTAURANT_DETAIL)

    def test_restaurant_detail_url_resolve_view_class(self):
        resolver_math = resolve(self.URL_RESTAURANT_DETAIL)
        self.assertEqual(resolver_math.view_name, self.URL_RESTAURANT_DETAIL_NAME)
        self.assertEqual(resolver_math.func.view_class, self.VIEW_CLASS)

    def test_restaurant_detail_page_before_restaurant_create(self):
        # 레스토랑 생성전 디테일 페이지에 들어갈 경우 오류가 잘 발생하는지 테스트
        url = reverse(self.URL_RESTAURANT_DETAIL_NAME, kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_detail(self):
        user = self.create_user()
        restaurant = self.create_restaurant(user=user)
        url = reverse(self.URL_RESTAURANT_DETAIL_NAME, kwargs={'pk': 1})
        self.assertEqual(url, self.URL_RESTAURANT_DETAIL)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(restaurant.pk, response.data['pk'])
        self.assertEqual(restaurant.owner_id, response.data['owner']['pk'])
        self.assertEqual(restaurant.favorite_set.count(), response.data['favorites'])
        #  get_favorite_count가 정상동작하는지 테스트
        self.assertEqual(restaurant.favorite_set.count(), restaurant.get_favorites_count())
