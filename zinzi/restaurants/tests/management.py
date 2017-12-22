from django.urls import reverse, resolve

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
