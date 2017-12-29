from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from accounts.models import Profile
from accounts.serializers import UserSerializer
from reservations.serializers.favorites import FavoriteSerializer, FavoriteRestaurantSerializer
from restaurants.models import Restaurant


class RestaurantFavoriteToggle(generics.GenericAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.profile.favorites.filter(pk=instance.pk):
            favorite_status = True
        else:
            favorite_status = False
        data = {
            'user': UserSerializer(user).data,
            'Restaurant': FavoriteRestaurantSerializer(instance).data,
            'result': favorite_status,
        }
        return Response(data)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.profile.favorites.filter(pk=instance.pk):
            user.profile.favorites.remove(instance)
            favorite_status = False
        else:
            user.profile.favorites.add(instance)
            favorite_status = True
        data = {
            'user': UserSerializer(user).data,
            'Restaurant': FavoriteRestaurantSerializer(instance).data,
            'result': favorite_status,
        }
        return Response(data)


class CustomerFavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Profile.objects.filter(user=self.request.user)
        return queryset
