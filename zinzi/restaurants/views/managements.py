from rest_framework import generics, permissions

from utils.permissions import IsOwnerOrNotAllow
from ..models import Restaurant
from ..serializers import RestaurantDetailSerializer

__all__ = (
    'ManagementRestaurant',
)


class ManagementRestaurant(generics.RetrieveUpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    permission_classes = (
        permissions.IsAdminUser,
        IsOwnerOrNotAllow,
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, args, kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(self, request, args, **kwargs)
