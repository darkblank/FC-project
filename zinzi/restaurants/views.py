from rest_framework import generics, permissions, mixins
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404

from utils.permissions import IsOwnerOrReadOnly, IsAuthorOrReadOnly
from .models import Restaurant, ReservationInfo, Comment
from .pagination import RestaurantListPagination, CommentListPagination
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
        queryset = Restaurant.objects.all()
        if restaurant_type is None and average_price is None:
            return queryset
        elif restaurant_type is None and average_price:
            return queryset.filter(average_price=average_price)
        elif restaurant_type and average_price is None:
            return queryset.filter(restaurant_type=restaurant_type)
        else:
            return queryset.filter(restaurant_type=restaurant_type, average_price=average_price)


class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    # 로그인을 하지 않았거나 Owner와 request.user가 같지 않을 경우 ReadOnly만 가능
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )


class CheckOpenedTimeView(generics.ListAPIView):
    serializer_class = ReservationInfoSerializer

    def get_queryset(self):
        # queryset에서 parameter값을 받아옴
        res_pk = self.kwargs['pk']
        party = self.request.query_params.get('party', None)
        date = self.request.query_params.get('date', None)
        queryset = ReservationInfo.check_acceptable_time(res_pk=res_pk, party=party, date=date)
        if queryset is None:
            raise ParseError('party 또는 date가 정상적으로 입력되지 않았습니다.')
        return queryset


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentListPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        res_pk = self.kwargs['pk']
        queryset = Comment.objects.filter(restaurant_id=res_pk)
        return queryset

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        serializer.save(restaurant=restaurant, author=self.request.user)
        restaurant.calculate_goten_star_rate()


class CommentUpdateDestroyView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
