from rest_framework import generics, permissions

from .models import Restaurant
from .pagination import RestaurantListPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import RestaurantSerializer


class RestaurantListView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    pagination_class = RestaurantListPagination

    def perform_create(self, serializer):
        # fixme - UserSerailizer가 없어 일단 request.user로 저장
        serializer.save(owner=self.request.user)


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    # 로그인을 하지 않았거나 Owner와 request.user가 같지 않을 경우 ReadOnly만 가능
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
