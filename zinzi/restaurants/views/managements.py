from rest_framework import generics

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantDetailSerializer
from utils.permissions import IsOwnerOrNotAllow

__all__ = (
    'ManagementRestaurant',
)


class ManagementRestaurant(generics.RetrieveUpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    permission_classes = (
        IsOwnerOrNotAllow,
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, args, kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(self, request, args, **kwargs)
