from rest_framework import serializers

from accounts.models import Profile
from accounts.serializers import UserSerializer
from restaurants.models import Restaurant


class FavoriteRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'pk',
            'name',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    favorites = FavoriteRestaurantSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            'user',
            'favorites',
        )
