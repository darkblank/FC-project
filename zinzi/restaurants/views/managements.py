from rest_framework import generics, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from restaurants.models import Restaurant, ImageForRestaurant
from restaurants.serializers import RestaurantDetailSerializer, ImageForRestaurantSerializer
from utils import permissions as custom_permissions

__all__ = (
    'ManagementRestaurantView',
    'ManagementRestaurantImageView',
)


class ManagementRestaurantView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    permission_classes = (
        custom_permissions.IsOwnerOrNotAllow,
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, args, kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, args, **kwargs)


class ManagementRestaurantImageView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ImageForRestaurant.objects.all()
    serializer_class = ImageForRestaurantSerializer
    permission_classes = (
        # fixme permission class가 무시되는 현상이 있음
        custom_permissions.IsOwnerForRestaurant,
    )

    def post(self, request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        if request.user != restaurant.owner:
            raise PermissionDenied('Owner가 아닙니다.')
        return self.create(request, args, kwargs)

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        serializer.save(restaurant=restaurant)
