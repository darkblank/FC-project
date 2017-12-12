from rest_framework import serializers

from reservations.models import Payment
from reservations.serializers import ReservationSerializer


class PaymentSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            '__all__'
        )