from rest_framework import generics, permissions
from rest_framework.exceptions import ParseError

from utils.permissions import IsOwnerOrReadOnly
from ..models import Restaurant, ReservationInfo
from ..pagination import RestaurantListPagination
from ..serializers import RestaurantListSerializer, RestaurantDetailSerializer, ReservationInfoSerializer

__all__ = (
    'RestaurantListView',
    'RestaurantDetailView',
    'CheckOpenedTimeView',
)


class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantListSerializer
    pagination_class = RestaurantListPagination

    # Querystring으로 전달된 type, price에 대해서 filter를 걸어 리턴하도록 설정
    # fixme district 필터를 추가해야함
    def get_queryset(self):
        q = self.request.query_params.get('q', None)
        if q:
            return Restaurant.get_searched_list(q=q)
        # querystring에서 type, price, district를 찾아 딕셔너리 형태로 Key에 대입, 없을경우 None객체를 넣음
        filter_fields = {
            'restaurant_type': self.request.query_params.get('type', None),
            'average_price': self.request.query_params.get('price', None),
            'district': self.request.query_params.get('district', None),
        }
        return Restaurant.get_filtered_list(filter_fields=filter_fields)


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
        # querystring에서 parameter값을 받아옴
        res_pk = self.kwargs['pk']
        party = self.request.query_params.get('party', None)
        date = self.request.query_params.get('date', None)
        queryset = ReservationInfo.check_acceptable_time(res_pk=res_pk, party=party, date=date)
        if queryset is None:
            raise ParseError('party 또는 date가 정상적으로 입력되지 않았습니다.')
        return queryset
