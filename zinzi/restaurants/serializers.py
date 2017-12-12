from rest_framework import serializers

from accounts.serializers import UserSerializer, ProfileImageSerializer
from .models import Restaurant, ImageForRestaurant, ReservationInfo, Comment


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
            'district',
            'restaurant_type',
            'average_price',
            'thumbnail',
            'star_rate',
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
            'geolocation',
            'contact_number',
            'description',
            'restaurant_type',
            'average_price',
            'thumbnail',
            'menu',
            'business_hours',
            'star_rate',
            'maximum_party',
            'owner',
            'images',
        )


class ReservationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationInfo
        fields = (
            'pk',
            'restaurant',
            'acceptable_size_of_party',
            'price',
            'time',
            'date',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileImageSerializer(read_only=True)
    # fixme 레스토랑을 입력받지 않고 저장을 할때 더 좋은 방법이 있는지 확인
    restaurant = serializers.CharField(required=False)

    class Meta:
        model = Comment
        fields = (
            'pk',
            'author',
            'restaurant',
            'star_rate',
            'comment',
            'created_at',
            'updated_at',
        )
