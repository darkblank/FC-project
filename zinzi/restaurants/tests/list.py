from random import randint

from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework import status

from restaurants.models import Restaurant, CHOICES_RESTAURANT_TYPE, CHOICES_PRICE
from restaurants.tests.base import RestaurantTestBase
from restaurants.views import RestaurantListView

User = get_user_model()


class RestaurantListViewTest(RestaurantTestBase):
    URL_RESTAURANT_LIST_NAME = 'restaurants:restaurant-list'
    URL_RESTAURANT_LIST = '/restaurants/'
    VIEW_CLASS = RestaurantListView

    def test_restaurant_list_url_name_reverse(self):
        url = reverse(self.URL_RESTAURANT_LIST_NAME)
        self.assertEqual(url, self.URL_RESTAURANT_LIST)

    def test_restaurant_list_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_RESTAURANT_LIST)
        self.assertEqual(resolver_match.view_name, self.URL_RESTAURANT_LIST_NAME)
        self.assertEqual(resolver_match.func.view_class, self.VIEW_CLASS)

    def http_method_check(self):
        url = reverse(self.URL_RESTAURANT_LIST_NAME)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        put_response = self.client.put(url)
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        patch_response = self.client.patch(url)
        self.assertEqual(patch_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_restaurant_list(self):
        user = self.create_user()
        num = randint(1, 10)
        for i in range(num):
            self.create_restaurant(user=user)
        url = reverse(self.URL_RESTAURANT_LIST_NAME)
        response = self.client.get(url)
        self.assertEqual(Restaurant.objects.count(), num)
        self.assertEqual(response.data['count'], num)
        for i in range(len(response.data['results'])):
            cur_restaurant_data = response.data['results'][i]
            self.assertIn('pk', cur_restaurant_data)
            self.assertIn('name', cur_restaurant_data)
            self.assertIn('address', cur_restaurant_data)
            self.assertIn('district', cur_restaurant_data)
            # geocoding으로 받아오는 주소가 강남구가 맞는지 확인
            self.assertEqual('강남구', cur_restaurant_data['district'])
            self.assertIn('geolocation', cur_restaurant_data)
            # default값인 star_rate가 0.0이 맞는지 확인
            self.assertEqual(cur_restaurant_data['star_rate'], '0.0')

    def test_get_restaurant_list_with_params(self):
        user = self.create_user()
        num = randint(1, 100)
        for i in range(num):
            self.create_restaurant(user=user)
        url = reverse(self.URL_RESTAURANT_LIST_NAME)
        params = {
            'type': CHOICES_RESTAURANT_TYPE[randint(0, len(CHOICES_RESTAURANT_TYPE) - 1)][0],
            'price': CHOICES_PRICE[randint(0, len(CHOICES_PRICE) - 1)][0],
        }
        # 필터된 리스트와 비교를 하기 위해 filter된 Restaurant List를 받아옴
        filtered_restaurant = Restaurant.objects.filter(restaurant_type=params['type'], average_price=params['price'])
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], filtered_restaurant.count())

        # 대문자 검색 테스트
        search_param_uppercase = {
            'q': 'DUMMY'
        }
        searched_upper_restaurant = Restaurant.get_searched_list(q=search_param_uppercase['q'])
        upper_response = self.client.get(url, search_param_uppercase)
        self.assertEqual(upper_response.status_code, status.HTTP_200_OK)
        self.assertEqual(upper_response.data['count'], searched_upper_restaurant.count())

        # 소문자 검색 테스트
        search_param_lowercase = {
            'q': 'dummy'
        }
        searched_lower_restaurant = Restaurant.get_searched_list(q=search_param_lowercase['q'])
        lower_response = self.client.get(url, search_param_lowercase)
        self.assertEqual(lower_response.status_code, status.HTTP_200_OK)
        self.assertEqual(lower_response.data['count'], searched_lower_restaurant.count())

        # 대문자 검색과 소문자 검색 결과가 같은지 테스트
        self.assertEqual(upper_response.data['count'], lower_response.data['count'])