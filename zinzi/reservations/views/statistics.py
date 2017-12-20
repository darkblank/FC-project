from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from rest_framework import generics
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from reservations.models import Payment
from restaurants.models import Restaurant
from utils.permissions import IsOwnerOrNotAllow

User = get_user_model()


class PaymentRateView(generics.GenericAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = (IsOwnerOrNotAllow,)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        paid = Payment.objects.filter(reservation__restaurant=instance)
        # cancelled_at이 0이 아닌 쿼리셋, 즉 취소되어진 시각이 존재하는 쿼리셋 필터링
        cancelled = paid.filter(~Q(cancelled_at=0))
        # round함수로 소수점 둘째자리에서 반올림
        data = {
            'payment rate': round(1 - (cancelled.count() / paid.count()), 2),
            'cancelled rate': round(cancelled.count() / paid.count(), 2),
        }
        return Response(data)


# 특정 레스토랑에 가장 많이 예약을 한 유저와 예약횟수 반환
class ReservationMVPView(generics.GenericAPIView):
    queryset = Restaurant.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        # 특정 레스토랑에 예약한 유저들 필터링
        reserved_user = User.objects.filter(reservation__restaurant=instance)
        # 필터링 되어진 유저들 중 해당 레스토랑에 가장 많이 예약한 유저를 mvp 변수에 담음
        mvp = reserved_user.annotate(reservation_count=Count('reservation')).order_by('-reservation_count').first()
        # mvp유저가 예약한 횟수
        mvp_count = mvp.reservation_count
        data = {
            'user': UserSerializer(mvp).data,
            'count': mvp_count,
        }
        return Response(data)
