from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Restaurant
from ..serializers import RestaurantDetailSerializer

__all__ = (
    'ManagementRestaurant',
)


class ManagementRestaurant(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    # fixme Owner인지 확인하는 퍼미션 필요
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )
