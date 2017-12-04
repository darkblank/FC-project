from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from .models import Restaurant, ReservationInfo, Comment
from .pagination import RestaurantListPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import RestaurantListSerializer, RestaurantDetailSerializer, ReservationInfoSerializer, \
    CommentSerializer


class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantListSerializer
    pagination_class = RestaurantListPagination

    # Querystring으로 전달된 type, price에 대해서 filter를 걸어 리턴하도록 설정
    # fixme district 필터를 추가해야함
    def get_queryset(self):
        restaurant_type = self.request.query_params.get('type', None)
        average_price = self.request.query_params.get('price', None)
        if not restaurant_type or not average_price:
            raise ValidationError('type 또는 price가 입력되지 않았습니다.')
        queryset = Restaurant.objects.filter(restaurant_type=restaurant_type, average_price=average_price)
        return queryset


class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    # 로그인을 하지 않았거나 Owner와 request.user가 같지 않을 경우 ReadOnly만 가능
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class CheckOpenedTimeView(generics.ListAPIView):
    serializer_class = ReservationInfoSerializer

    def get_queryset(self):
        # queryset에서 parameter값을 받아옴
        res_pk = self.request.query_params.get('res_pk', None)
        party = self.request.query_params.get('party', None)
        date = self.request.query_params.get('date', None)
        return ReservationInfo.check_acceptable_time(res_pk=res_pk, party=party, date=date)


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    # fixme permission 작성해야함

    def get_queryset(self):
        res_pk = self.kwargs['res_pk']
        queryset = Comment.objects.filter(restaurant_id=res_pk)
        return queryset

    def perform_create(self, serializer):
        # fixme author에 request.user 넣어야
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['res_pk'])
        serializer.save(restaurant=restaurant)
        restaurant.calculate_goten_star_rate()

