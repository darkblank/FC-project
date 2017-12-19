from datetime import datetime
from random import randint

from django.urls import reverse, resolve
from rest_framework import status

from restaurants.models import CHOICES_TIME, ReservationInfo
from restaurants.tests.base import RestaurantTestBase
from restaurants.views import CheckOpenedTimeView


class CheckOpenedTimeViewTest(RestaurantTestBase):
    URL_CHECK_OPENED_TABLE_NAME = 'restaurants:check-time'
    URL_CHECK_OPENED_TABLE = '/restaurants/1/check_opened_time/'
    VIEW_CLASS = CheckOpenedTimeView

    def create_info(self):
        num = randint(0, len(CHOICES_TIME))
        restaurant = self.create_restaurant()
        for i in range(num):
            ReservationInfo.objects.create(
                restaurant=restaurant,
                price=CHOICES_TIME[i],
                date=datetime.now().date()
            )
        return ReservationInfo.objects.all()

    def test_check_opened_time_url_name_reverse(self):
        url = reverse(self.URL_CHECK_OPENED_TABLE_NAME, kwargs={'pk': 1})
        self.assertEqual(url, self.URL_CHECK_OPENED_TABLE)

    def test_check_opened_time_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_CHECK_OPENED_TABLE)
        self.assertEqual(resolver_match.view_name, self.URL_CHECK_OPENED_TABLE_NAME)
        self.assertEqual(resolver_match.func.view_class, self.VIEW_CLASS)

    def http_method_check(self):
        url = reverse(self.URL_CHECK_OPENED_TABLE_NAME, kwargs={'pk': 1})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)