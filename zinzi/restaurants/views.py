from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from .models import Restaurant
from .pagination import RestaurantListPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import RestaurantListSerializer, RestaurantDetailSerializer


class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantListSerializer
    pagination_class = RestaurantListPagination

    # Querystring으로 전달된 type, price에 대해서 filter를 걸어 리턴하도록 설정
    # fixme district 필터를 추가해야함
    def get_queryset(self):
        restaurant_type = self.request.query_params.get('type', None)
        average_price = self.request.query_params.get('price', None)
        if not restaurant_type or not average_price:
            raise ValidationError
        queryset = Restaurant.objects.filter(restaurant_type=restaurant_type, average_price=average_price)
        return queryset


class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    # 로그인을 하지 않았거나 Owner와 request.user가 같지 않을 경우 ReadOnly만 가능
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
