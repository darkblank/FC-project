from rest_framework import generics, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from restaurants.models import Restaurant, ImageForRestaurant, MenuImages
from restaurants.serializers import RestaurantDetailSerializer, ImageForRestaurantSerializer, MenuImagesSerializer
from utils import permissions as custom_permissions

__all__ = (
    'ManagementRestaurantView',
    'CreateRestaurantImageView',
    'UpdateDestroyRestaurantImageView',
    'CreateRestaurantMenuView',
    'UpdateDestroyRestaurantMenuView',
)


class ManagementRestaurantView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    permission_classes = (
        custom_permissions.IsOwnerOrNotAllow,
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateRestaurantImageView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ImageForRestaurant.objects.all()
    serializer_class = ImageForRestaurantSerializer
    permission_classes = (
        custom_permissions.IsOwnerForRestaurant,
    )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        serializer.save(restaurant=restaurant)


class UpdateDestroyRestaurantImageView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = ImageForRestaurant.objects.all()
    serializer_class = ImageForRestaurantSerializer
    permission_classes = (
        custom_permissions.IsOwnerForRestaurant,
    )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CreateRestaurantMenuView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = MenuImages.objects.all()
    serializer_class = MenuImagesSerializer
    permission_classes = (
        custom_permissions.IsOwnerForRestaurant,
    )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        serializer.save(restaurant=restaurant)


class UpdateDestroyRestaurantMenuView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = MenuImages.objects.all()
    serializer_class = MenuImagesSerializer
    permission_classes = (
        custom_permissions.IsOwnerForRestaurant,
    )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
