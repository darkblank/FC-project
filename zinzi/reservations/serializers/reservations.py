from rest_framework import serializers

from accounts.serializers import UserSerializer
from reservations.models import Reservation
from restaurants.models import ReservationInfo, Restaurant


class RestaurantCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'pk',
            'name',
            'address',
            'thumbnail',
        )


class ReservationInfoCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationInfo
        fields = (
            'pk',
            'time',
            'date',
        )


class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    information = ReservationInfoCustomSerializer(read_only=True)
    restaurant = RestaurantCustomSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = (
            'pk',
            'name',
            'party',
            'price',
            'phone_number',
            'email',
            'status',
            'user',
            'information',
            'restaurant',
        )
