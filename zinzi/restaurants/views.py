from rest_framework import generics, permissions

from .models import Restaurant
from .pagination import RestaurantListPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import RestaurantListSerializer, RestaurantDetailSerializer


class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer
    pagination_class = RestaurantListPagination


class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    # 로그인을 하지 않았거나 Owner와 request.user가 같지 않을 경우 ReadOnly만 가능
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
