from rest_framework import generics, permissions

from utils.permissions import IsOwnerOrNotAllow
from ..models import Restaurant
from ..serializers import RestaurantDetailSerializer

__all__ = (
    'ManagementRestaurant',
)


class ManagementRestaurant(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    permission_classes = (
        permissions.IsAdminUser,
        IsOwnerOrNotAllow,
    )
