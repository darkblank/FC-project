from rest_framework import serializers

from accounts.serializers import UserSerializer
from reservations.models import Reservation
from restaurants.serializers import ReservationInfoSerializer, RestaurantListSerializer


class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    information = ReservationInfoSerializer(read_only=True)
    restaurant = RestaurantListSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = (
            '__all__'
        )