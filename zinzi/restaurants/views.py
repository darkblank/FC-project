from rest_framework import generics

from .models import Restaurant
from .pagination import RestaurantListPagination
from .serializers import RestaurantSerializer


class RestaurantListView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    pagination_class = RestaurantListPagination

    def perform_create(self, serializer):
        # fixme - UserSerailizer가 없어 일단 request.user로 저장
        serializer.save(owner=self.request.user)
