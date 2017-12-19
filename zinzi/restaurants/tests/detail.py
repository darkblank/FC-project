from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework import status

from restaurants.tests import RestaurantTestBase
from restaurants.views import RestaurantDetailView

User = get_user_model()


class RestaurantDetailViewTest(RestaurantTestBase):
    URL_RESTAURANT_DETAIL_NAME = 'restaurants:restaurant-detail'
    URL_RESTAURANT_DETAIL = '/restaurants/1/'
    VIEW_CLASS = RestaurantDetailView

    def test_restaurant_detail_url_name_reverse(self):
        url = reverse(self.URL_RESTAURANT_DETAIL_NAME, kwargs={'pk': 1})
        self.assertEqual(url, self.URL_RESTAURANT_DETAIL)

    def test_restaurant_detail_url_resolve_view_class(self):
        resolver_math = resolve(self.URL_RESTAURANT_DETAIL)
        self.assertEqual(resolver_math.view_name, self.URL_RESTAURANT_DETAIL_NAME)
        self.assertEqual(resolver_math.func.view_class, self.VIEW_CLASS)

    def http_method_check(self):
        url = reverse(self.URL_RESTAURANT_DETAIL_NAME)
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
