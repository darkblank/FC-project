from rest_framework import serializers

from members.serializers import UserSerializer
from .models import Restaurant, ImageForRestaurant


class ImageForRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageForRestaurant
        fields = (
            'image',
        )


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'pk',
            'name',
            'address',
            'geolocation',
            'restaurant_type',
            'average_price',
            'thumbnail',
        )


class RestaurantDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    images = ImageForRestaurantSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = (
            'pk',
            'name',
            'address',
            'menu',
            'geolocation',
            'contact_number',
            'description',
            'restaurant_type',
            'average_price',
            'thumbnail',
            'images',
            'owner',
        )
