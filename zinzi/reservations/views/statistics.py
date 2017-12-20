from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from reservations.models import Payment
from restaurants.models import Restaurant
from utils.permissions import IsOwnerOrNotAllow


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
            'payment rate': round(cancelled.count() / paid.count(), 2),
            'cancelled rate': round(1 - (cancelled.count() / paid.count()), 2),
        }
        return Response(data)
