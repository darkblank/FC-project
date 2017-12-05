from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Restaurant, ImageForRestaurant, ReservationInfo, Comment


class ImageForRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageForRestaurant
        fields = (
            'image',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'author',
            'restaurant',
            'star_rate',
            'comment',
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
    comments = CommentSerializer(many=True)

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
            'comments',
        )


class ReservationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationInfo
        fields = (
            'restaurant',
            'acceptable_size_of_party',
            'price',s
            'time',
            'date',
        )
