from rest_framework import serializers

from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    # fixme
    # owner = UserSerializer(read_only=True)
    class Meta:
        model = Restaurant
        fields = (
            'name',
            'city',
            'district',
            'detail_address',
            'contact_number',
            'joined_date',
            'description',
            'restaurant_type',
            'average_price',
            'thumbnail',
            # fixme
            'owner',
        )
