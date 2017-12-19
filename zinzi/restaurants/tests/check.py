from datetime import datetime, timedelta

from django.urls import reverse, resolve
from rest_framework import status

from restaurants.models import CHOICES_TIME, ReservationInfo
from restaurants.tests import RestaurantTestBase
from restaurants.views import CheckOpenedTimeView


class CheckOpenedTimeViewTest(RestaurantTestBase):
    URL_CHECK_OPENED_TIME_NAME = 'restaurants:check-time'
    URL_CHECK_OPENED_TIME = '/restaurants/1/check_opened_time/'
    VIEW_CLASS = CheckOpenedTimeView

    @staticmethod
    def create_info(restaurant, date=None):
        if not date:
            date = datetime.today()
        num = len(CHOICES_TIME)
        for i in range(num):
            ReservationInfo.objects.create(
                restaurant=restaurant,
                date=date,
                time=CHOICES_TIME[i][0],
            )
        return ReservationInfo.objects.all()



    def test_restaurant_detail_url_name_reverse(self):
        url = reverse(self.URL_CHECK_OPENED_TIME_NAME, kwargs={'pk': 1})
        self.assertEqual(url, self.URL_CHECK_OPENED_TIME)

    def test_restaurant_detail_url_resolve_view_class(self):
        resolver_math = resolve(self.URL_CHECK_OPENED_TIME)
        self.assertEqual(resolver_math.view_name, self.URL_CHECK_OPENED_TIME_NAME)
        self.assertEqual(resolver_math.func.view_class, self.VIEW_CLASS)

    def test_method_check(self):
        restaurant = self.create_restaurant(user=self.create_user())
        self.create_info(restaurant=restaurant)
        url = reverse(self.URL_CHECK_OPENED_TIME_NAME,
                      kwargs={'pk': restaurant.pk}) + '?party=1&date=' + datetime.today().strftime('%Y-%m-%d')
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

    def test_get_request_without_params(self):
        restaurant = self.create_restaurant(user=self.create_user())
        url = reverse(self.URL_CHECK_OPENED_TIME_NAME, kwargs={'pk': restaurant.pk})
        url_without_date = url + '?party=1'
        without_date_response = self.client.get(url_without_date)
        self.assertEqual(without_date_response.status_code, status.HTTP_400_BAD_REQUEST)
        url_without_party = url + '?date=' + datetime.today().strftime('%Y-%m-%d')
        without_party_response = self.client.get(url_without_party)
        self.assertEqual(without_party_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_request_with_wrong_params(self):
        restaurant = self.create_restaurant(user=self.create_user())
        self.create_info(restaurant=restaurant)
        today = datetime.today()
        url = reverse(self.URL_CHECK_OPENED_TIME_NAME, kwargs={'pk': restaurant.pk})
        wrong_params = (
            {'party': 'one',
             'date': today.strftime('%Y-%m-%d')},
            {'party': '1',
             'date': today.strftime('%m-%d')},
            {'party': '1',
             'date': today.strftime('%Y-%d')},
            {'party': '1',
             'date': today.strftime('%Y-%m')},
            {'party': '1',
             'date': today.strftime('%Y/%m/%d')},
            {'party': 'one',
             'date': today.strftime('%Y.%m/%d')},
        )
        for wrong_param in wrong_params:
            url_with_wrong_param = url + '?party' + wrong_param['party'] + '&date' + wrong_param['date']
            response_with_wrong_param = self.client.get(url_with_wrong_param)
            self.assertEqual(response_with_wrong_param.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_opened_time_today(self):
        restaurant = self.create_restaurant(user=self.create_user())
        self.create_info(restaurant=restaurant)
        party = str(1)
        date = datetime.today().strftime('%Y-%m-%d')
        url = reverse(self.URL_CHECK_OPENED_TIME_NAME,
                      kwargs={'pk': restaurant.pk}) + '?party=' + party + '&date=' + date
        response = self.client.get(url)
        # 오늘 일 경우 데이터가 현재 시간 이후의 것만 나와야 하기때문에 filter한 Info와 response.data의 길이가 같은지 확인
        self.assertEqual(
            ReservationInfo.objects.filter(acceptable_size_of_party__gte=party,
                                           date=datetime.now().date(),
                                           time__hour__gt=(datetime.now() + timedelta(hours=9)).hour).count(),
            len(response.data)
        )
        for cur_data in response.data:
            self.assertIn('pk', cur_data)
            self.assertIn('restaurant', cur_data)
            self.assertIn('acceptable_size_of_party', cur_data)
            self.assertIn('price', cur_data)
            self.assertIn('time', cur_data)
            self.assertIn('date', cur_data)

    def test_check_opened_time_tomorrow(self):
        tomorrow = datetime.today() + timedelta(days=1)
        restaurant = self.create_restaurant()
        self.create_info(restaurant=restaurant, date=tomorrow)
        party = str(1)
        date = tomorrow.strftime('%Y-%m-%d')
        url = reverse(self.URL_CHECK_OPENED_TIME_NAME,
                      kwargs={'pk': restaurant.pk}) + '?party=' + party + '&date=' +date
        response = self.client.get(url)
        self.assertEqual(
            ReservationInfo.objects.filter(acceptable_size_of_party__gte=party,
                                           date=tomorrow.date()).count(),
            len(response.data)
        )
        



