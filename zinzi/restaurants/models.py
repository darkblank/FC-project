from datetime import time, datetime

import dateutil.parser
from django.db import models
from django.db.models import Sum
from django_google_maps import fields as map_fields
from rest_framework.exceptions import ValidationError
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
    # fixme requests로 받아올 수 있게 처리
    geolocation = map_fields.GeoLocationField(max_length=100)
    # fixme 연락처 정규표현식으로 만들기
    contact_number = models.CharField(max_length=11)
    joined_date = models.DateField(auto_now_add=True)
    description = models.TextField()
    restaurant_type = models.CharField(max_length=3, choices=CHOICES_RESTAURANT_TYPE)
    average_price = models.CharField(max_length=1, choices=CHOICES_PRICE)
    thumbnail = models.ImageField(upload_to='thumbnail')
    menu = models.ImageField(upload_to='menu')
    business_hours = models.CharField(max_length=100)
    star_rate = models.DecimalField(null=False, blank=True, default=0, decimal_places=1, max_digits=2)
    maximum_party = models.PositiveIntegerField()
    owner = models.ForeignKey('accounts.User')

    def __str__(self):
        return self.name

    def calculate_goten_star_rate(self):
        queryset = Comment.objects.filter(restaurant=self)
        star_rate = queryset.aggregate(Sum('star_rate'))
        count_star_rate = queryset.count()
        self.star_rate = star_rate['star_rate__sum'] / count_star_rate
        self.save()
        return star_rate


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
    @staticmethod
    def check_acceptable_time(res_pk, party, date):
        restaurant = get_object_or_404(Restaurant, pk=res_pk)
        # string으로 온 date값을 python에서 사용하는 datetime type으로 파싱 진행
        # 파싱을 진행하며 잘못된 값이 올 경우 None객체 반환
        try:
            parsed_date = dateutil.parser.parse(date)
        except ValueError:
            parsed_date = None
        except TypeError:
            parsed_date = None
        # 모든 parameter가 정상적인 경우 필터된 객체를 반환
        # party가 숫자가 아닌경우, parsed_date가 datetime type이 아닌 경우 None객체를 반환
        if not party:
            return None
        if party.isdigit() and isinstance(parsed_date, datetime):
            return ReservationInfo.objects.filter(
                restaurant=restaurant,
                acceptable_size_of_party__gte=party,
                date=date,
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
