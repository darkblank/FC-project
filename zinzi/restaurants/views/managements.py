from rest_framework import generics, mixins

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantDetailSerializer
from utils.permissions import IsOwnerOrNotAllow

__all__ = (
    'ManagementRestaurantView',
)


class ManagementRestaurantView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    permission_classes = (
        IsOwnerOrNotAllow,
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, args, kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, args, **kwargs)
