from django.urls import reverse, resolve
from rest_framework import status

from restaurants.tests import RestaurantTestBase
from restaurants.views import ManagementRestaurantView

__all__ = (
    'ManagementViewTest',
)


class ManagementViewTest(RestaurantTestBase):
    URL_MANAGEMENT_RETRIEVE_NAME = 'restaurants:management:management-restaurant'
    URL_MANAGEMENT_RETRIEVE = '/restaurants/management/1/'
    VIEW_CLASS = ManagementRestaurantView

    def test_management_url_name_reverse(self):
        url = reverse(self.URL_MANAGEMENT_RETRIEVE_NAME, kwargs={'pk': 1})
        self.assertEqual(url, self.URL_MANAGEMENT_RETRIEVE)

    def test_management_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_MANAGEMENT_RETRIEVE)
        self.assertEqual(resolver_match.view_name, self.URL_MANAGEMENT_RETRIEVE_NAME)
        self.assertEqual(resolver_match.func.view_class, self.VIEW_CLASS)

    def test_method_check_with_permission(self):
        user = self.create_user()
        restaurant = self.create_restaurant(user=user)
        url = reverse(self.URL_MANAGEMENT_RETRIEVE_NAME, kwargs={'pk': restaurant.pk})
        self.client.force_authenticate(user=user)
        self.client.force_login(user=user)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        put_response = self.client.put(url)
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        patch_response = self.client.patch(url)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_method_check_without_permission(self):
        user = self.create_user()
        user2 = self.create_user2()
        restaurant = self.create_restaurant(user=user)
        url = reverse(self.URL_MANAGEMENT_RETRIEVE_NAME, kwargs={'pk': restaurant.pk})
        self.client.force_authenticate(user=user2)
        self.client.force_login(user=user2)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_403_FORBIDDEN)
        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        put_response = self.client.put(url)
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        patch_response = self.client.patch(url)
        self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)
        delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_method_restaurant_management(self):
        user = self.create_user()
        restaurant = self.create_restaurant(user=user)
        url = reverse(self.URL_MANAGEMENT_RETRIEVE_NAME, kwargs={'pk': restaurant.pk})
        self.client.force_authenticate(user=user)
        self.client.force_login(user=user)
        response = self.client.get(url)
        self.assertIn('pk', response.data)
        self.assertIn('name', response.data)
        self.assertIn('address', response.data)
        self.assertIn('geolocation', response.data)
        self.assertIn('contact_number', response.data)
        self.assertIn('description', response.data)
        self.assertIn('restaurant_type', response.data)
        self.assertIn('average_price', response.data)
        self.assertIn('favorites', response.data)
        self.assertEqual(0, response.data['favorites'])
        self.assertIn('thumbnail', response.data)
        self.assertIn('menu', response.data)
        self.assertIn('business_hours', response.data)
        self.assertIn('star_rate', response.data)
        self.assertEqual("0.0", response.data['star_rate'])
        self.assertIn('maximum_party', response.data)
        self.assertIn('owner', response.data)
        self.assertIn('image', response.data)

