import re
from datetime import time, datetime, timedelta

import dateutil.parser
import requests
from django.conf import settings
from django.db import models
from django.db.models import Avg
from django_google_maps import fields as map_fields
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.generics import get_object_or_404

CHOICES_RESTAURANT_TYPE = (
    ('kor', 'Korean'),
    ('chn', 'Chinese'),
    ('jpn', 'Japanese'),
    ('mex', 'Mexican'),
    ('amc', 'American'),
    ('tha', 'Thai'),
    ('med', 'Mediterranean'),
    ('ita', 'Italian'),
    ('vtn', 'Vietnamese'),
    ('spn', 'Spanish'),
    ('ind', 'Indian'),
    ('etc', 'Etc'),
)
CHOICES_PRICE = (
    ('c', 'Cheap'),
    ('n', 'Normal'),
    ('e', 'Expensive'),
    ('v', 'Very Expensive'),
)
CONVERT_TO_PRICE = {
    'c': 10000,
    'n': 15000,
    'e': 20000,
    'v': 40000,
}
CHOICES_TIME = (
    (time(9, 00, 00), '9시'),
    (time(10, 00, 00), '10시'),
    (time(11, 00, 00), '11시'),
    (time(12, 00, 00), '12시'),
    (time(13, 00, 00), '13시'),
    (time(14, 00, 00), '14시'),
    (time(15, 00, 00), '15시'),
    (time(16, 00, 00), '16시'),
    (time(17, 00, 00), '17시'),
    (time(18, 00, 00), '18시'),
    (time(19, 00, 00), '19시'),
    (time(20, 00, 00), '20시'),
    (time(21, 00, 00), '21시'),
)

STAR_RATING = (
    (0, 0),
    (0.5, 0.5),
    (1, 1),
    (1.5, 1.5),
    (2, 2),
    (2.5, 2.5),
    (3, 3),
    (3.5, 3.5),
    (4, 4),
    (4.5, 4.5),
    (5, 5),
)


# 이름 리뷰 평점 즐겨찾기 토글, 소개, 메뉴, 음식 사진, 주소, 전화번호, 영업 시간, 가격대 <
# 평점 토글, 댓글 <
# 예약 <

class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    address = map_fields.AddressField(max_length=200)
    district = models.CharField(null=False, blank=True, max_length=20)
    geolocation = map_fields.GeoLocationField(max_length=100)
    # fixme 연락처 정규표현식으로 만들기
    contact_number = models.CharField(max_length=11)
    joined_date = models.DateField(auto_now_add=True)
    description = models.TextField()
    restaurant_type = models.CharField(max_length=3, choices=CHOICES_RESTAURANT_TYPE)
    average_price = models.CharField(max_length=1, choices=CHOICES_PRICE)
    thumbnail = models.ImageField(upload_to='thumbnail')
    # fixme menu image model 추가
    menu = models.ImageField(upload_to='menu')
    business_hours = models.CharField(max_length=100)
    star_rate = models.DecimalField(null=False, blank=True, default=0, decimal_places=1, max_digits=2)
    maximum_party = models.PositiveIntegerField()
    owner = models.ForeignKey('accounts.User')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.district:
            # Google goecoding에 검색할 parameter값 지정
            params = {
                'address': self.address,
                'language': 'ko'
            }
            res = requests.get(settings.GOOGLE_MAPS_API_URL, params=params).json()
            # 반환되는 값에서 구가 들어오는 위치의 값 추출(정상적으로 입력하였을 경우)
            district = res['results'][0]['address_components'][2]['long_name']
            # 정규표현식으로 추출하여 '구'로 끝나는지 값을 찾아 re_district에 저장
            re_district = re.search('\w{2,3}구', district)
            # None Type일 경우 즉, 정규표현식에서 '구'로 끝나는 값을 찾지 못했을 경우 ValueError를 일으킴
            if re_district is None:
                raise ValueError('구 입력이 정상적이지 않습니다.')
            self.district = re_district.group()
        return super().save(*args, **kwargs)

    # 댓글 작성시 호출됨
    def calculate_goten_star_rate(self):
        queryset = Comment.objects.filter(restaurant=self)
        # 쿼리셋의 aggregation기능을 사용해 평균값을 계산
        star_rate = queryset.aggregate(Avg('star_rate'))
        # aggregation은 딕셔너리 형태로 나오므로 키값을 넣어 value를 star_rate에 넣고 저장
        self.star_rate = star_rate['star_rate__avg']
        self.save()

    @classmethod
    def get_filtered_list(cls, res_type, price):
        queryset = cls.objects.all()
        if res_type is None and price is None:
            return queryset
        elif res_type is None and price:
            return queryset.filter(average_price=price)
        elif res_type and price is None:
            return queryset.filter(restaurant_type=res_type)
        else:
            return queryset.filter(restaurant_type=res_type, average_price=price)


class ImageForRestaurant(models.Model):
    image = models.ImageField(upload_to='restaurant')
    restaurant = models.ForeignKey('Restaurant', related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.restaurant} - {self.pk}'


class ReservationInfo(models.Model):
    restaurant = models.ForeignKey('Restaurant', related_name='reservation_info', on_delete=models.CASCADE)
    acceptable_size_of_party = models.IntegerField(null=False, blank=True)
    price = models.PositiveIntegerField(null=False, blank=True)
    time = models.TimeField(choices=CHOICES_TIME)
    date = models.DateField()

    def __str__(self):
        return f'{self.restaurant} - [{self.date}-{self.time}]'

    def save(self, *args, **kwargs):
        if ReservationInfo.objects.filter(restaurant=self.restaurant, time=self.time, date=self.date).count():
            raise ValueError('This ReservationInfo is already exist')
        # acceptable_size_of_party에 값이 없을 경우 자동으로 restaurant.maximum_party에서 값을 받아와서 저장
        if self.acceptable_size_of_party is None:
            self.acceptable_size_of_party = self.restaurant.maximum_party
        self.price = CONVERT_TO_PRICE[self.restaurant.average_price]
        return super().save(*args, **kwargs)

    def calculate_price(self, party):
        if party.isdigit() and party <= self.acceptable_size_of_party:
            return self.price * party
        raise ValidationError

    # 예약시 호출하여 해당 시간의 허용 가능한 인원수를 수정할수 있게 할 수 있는 메서드생성
    def acceptable_size_of_party_update(self, party):
        if isinstance(party, int):
            self.acceptable_size_of_party -= party
            self.save()
            return True
        raise ValidationError('party가 int 형식이 아닙니다.')

    # CheckOpenedTimeView의 get_queryset에서 호출하여 valid한지 검증 valid하지 않을 경우 None 반환
    @classmethod
    def check_acceptable_time(cls, res_pk, party, date):
        restaurant = get_object_or_404(Restaurant, pk=res_pk)
        # string으로 온 date값을 python에서 사용하는 datetime type으로 파싱 진행
        # 파싱을 진행하며 잘못된 값이 올 경우 None객체 반환
        try:
            parsed_date = dateutil.parser.parse(date)
        except ValueError:
            parsed_date = None
        except TypeError:
            parsed_date = None
        try:
            if date != parsed_date.strftime('%Y-%m-%d'):
                raise ParseError('date의 형식이 맞지 않습니다.')
        except AttributeError:
            raise ParseError('date의 형식이 맞지 않습니다.')
        # 모든 parameter가 정상적인 경우 필터된 객체를 반환
        # party가 숫자가 아닌경우, parsed_date가 datetime type이 아닌 경우 None객체를 반환
        if not party and parsed_date is None:
            return None
        # 금일보다 적은 날짜인지 비교를 위해 datetime.now(UTC)에서 9시간을 더 한(한국시간)시간을 불러와 원하는 형식인 YYYY-MM-DD형식으로 변경후 datetime 형태로 다시 파싱
        # 검색했던 날짜가 파싱된 datetime.now와 비교하여 작은경우(오늘보다 이전인경우) 검색이 되지 않도록 변경
        now_date = datetime.now() + timedelta(hours=9)
        parsed_now_date = dateutil.parser.parse((datetime.now() + timedelta(hours=9)).strftime('%Y-%m-%d'))
        if parsed_date < parsed_now_date:
            raise ParseError('date가 오늘보다 이전입니다.')
        if parsed_date.date() == now_date.date():
            return cls.objects.filter(
                restaurant=restaurant,
                acceptable_size_of_party__gte=party,
                date=parsed_date,
                # fixme time 필터 추가 필요 (금일 일 경우 현재 시간보다 이전만 가능하게)
                time__hour__gt=now_date.hour,
            )
        if party.isdigit() and parsed_date:
            return cls.objects.filter(
                restaurant=restaurant,
                acceptable_size_of_party__gte=party,
                date=parsed_date,
            )
        return None


class Comment(models.Model):
    author = models.ForeignKey('accounts.User')
    restaurant = models.ForeignKey('Restaurant', related_name='comments', on_delete=models.CASCADE)
    star_rate = models.FloatField(choices=STAR_RATING)
    comment = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at', 'pk')

    def __str__(self):
        return f'{self.author.email} - {self.restaurant} [{self.created_at}]'
