from django.contrib.postgres.fields import ArrayField
from django.db import models

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


class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    city = models.CharField(max_length=5)
    district = models.CharField(max_length=5)
    detail_address = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=11)
    joined_date = models.DateField(auto_now_add=True)
    description = models.TextField()
    restaurant_type = models.CharField(max_length=3, choices=CHOICES_RESTAURANT_TYPE)
    average_price = models.CharField(max_length=1, choices=CHOICES_PRICE)
    thumbnail = models.ImageField()
    owner = models.ForeignKey('members.User')
    # available = ArrayField(
    #     models.TimeField()
    # )

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField(max_length=7)
    image = models.ImageField()
    restaurant = models.ForeignKey('Restaurant')

    def __str__(self):
        return f'{self.restaurant.name} - {self.name}'


class ImageForRestaurant(models.Model):
    image = models.ImageField()
    restaurant = models.ForeignKey(Restaurant)
