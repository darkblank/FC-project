from rest_framework import serializers

from accounts.serializers import UserSerializer, ProfileImageSerializer
from .models import Restaurant, ImageForRestaurant, ReservationInfo, Comment, MenuImages, CONVERT_TO_PRICE


class ImageForRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageForRestaurant
        fields = (
            'pk',
            'image',
        )


class MenuImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuImages
        fields = (
            'pk',
            'image',
        )


class RestaurantListSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

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

    def get_thumbnail(self, obj):
        return obj.main_image_thumbnail.url


class RestaurantDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    images = ImageForRestaurantSerializer(read_only=True, many=True)
    menu = MenuImagesSerializer(read_only=True, many=True)
    favorites = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

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
            'price',
            'favorites',
            'thumbnail',
            'menu',
            'business_hours',
            'star_rate',
            'maximum_party',
            'owner',
            'images',
        )

    def get_favorites(self, obj):
        return obj.get_favorites_count()

    def get_price(self, obj):
        return CONVERT_TO_PRICE[obj.average_price]

    def get_thumbnail(self, obj):
        return obj.main_image_thumbnail.url


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
