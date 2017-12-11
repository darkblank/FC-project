from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from iamport import Iamport
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Reservation, Payment
from reservations.serializers import PaymentSerializer, ReservationSerializer
from restaurants.models import ReservationInfo, Restaurant

User = get_user_model()


def test(request):
    return render(request, 'test.html')


class ReservationCreateView(generics.GenericAPIView,
                            mixins.CreateModelMixin,
                            ):
    serializer_class = ReservationSerializer
    queryset = ReservationInfo.objects.all()

    def perform_create(self, serializer):
        information = self.get_object()
        serializer.save(
            user=self.request.user,
            information=information,
            restaurant=information.restaurant,
        )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReservationPatchView(generics.UpdateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class CustomerReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = Reservation.objects.filter(user=self.request.user)
        return queryset


class CustomerReservationDetailView(generics.RetrieveAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = Reservation.objects.filter(user=self.request.user)
        return queryset


class RestaurantReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        restaurant = get_object_or_404(Restaurant, pk=pk)
        queryset = Reservation.objects.filter(restaurant=restaurant)
        return queryset


class RestaurantReservationDetailView(generics.RetrieveAPIView):
    serializer_class = ReservationSerializer
    lookup_url_kwarg = 'reserve_pk'

    def get_queryset(self):
        pk = self.kwargs['pk']
        restaurant = get_object_or_404(Restaurant, pk=pk)
        queryset = Reservation.objects.filter(restaurant=restaurant)
        return queryset


# 가격 불일치시 메일이나 문자 보내주는 메서드도 추가 필요
# status==paid 인지 확인 필요
class PaymentCreateView(APIView):
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        iamport = Iamport(imp_key=settings.IMP_KEY,
                          imp_secret=settings.IMP_SECRET)
        payment = iamport.find(imp_uid=request.data.get('imp_uid'))
        if not iamport.is_paid(int(request.data.get('price')), imp_uid=request.data.get('imp_uid')):
            cancel = iamport.cancel(u'가격 불일치', imp_uid=request.data.get('imp_uid'))
            serializer = PaymentSerializer(data=cancel)
        else:
            serializer = PaymentSerializer(data=payment)
        if serializer.is_valid():
            serializer.save(reservation=reservation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'imp_uid'
