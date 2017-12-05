from rest_framework import serializers

from accounts.serializers import UserSerializer
from reservations.models import Payment, Reservation
from restaurants.serializers import ReservationInfoSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            '__all__',
        )


class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    information = ReservationInfoSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = (
            '__all__',
        )
