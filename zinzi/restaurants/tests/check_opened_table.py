from django.urls import reverse, resolve

from restaurants.tests import RestaurantTestBase
from restaurants.views import CheckOpenedTimeView


class CheckOpenedTimeViewTest(RestaurantTestBase):
    URL_CHECK_OPENED_TABLE_NAME = 'restaurants:check-time'
    URL_CEHCK_OPENED_TABLE = '/restaurants/1/check_opened_time/'
    VIEW_CLASS = CheckOpenedTimeView

    def test_check_opened_time_url_name_reverse(self):
        url = reverse(self.URL_CHECK_OPENED_TABLE_NAME, kwargs={'pk': 1})
        self.assertEqual(url, self.URL_CEHCK_OPENED_TABLE)

    def test_check_opened_time_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_CEHCK_OPENED_TABLE)
        self.assertEqual(resolver_match.view_name, self.URL_CHECK_OPENED_TABLE_NAME)
        self.assertEqual(resolver_match.func.view_class, self.VIEW_CLASS)
