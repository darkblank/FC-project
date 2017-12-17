from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import exceptions
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Reservation, Payment
from reservations.serializers import ReservationSerializer
from reservations.serializers.payments import PaymentSerializer
from restaurants.models import ReservationInfo, Restaurant
from utils.permissions import IsUserOrNotAllow, NotAllowForSpecificData

User = get_user_model()


class ReservationCreateView(generics.GenericAPIView,
                            mixins.CreateModelMixin,
                            ):
    serializer_class = ReservationSerializer
    queryset = ReservationInfo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

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
    permission_classes = (
        IsUserOrNotAllow,
        NotAllowForSpecificData,
    )


class CustomerReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Reservation.objects.filter(user=self.request.user)
        return queryset


class CustomerReservationDetailView(generics.RetrieveAPIView):
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Reservation.objects.filter(user=self.request.user)
        return queryset


class RestaurantReservationListView(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        restaurant = get_object_or_404(Restaurant, pk=pk)
        queryset = Payment.objects.filter(reservation__restaurant=restaurant)
        return queryset


class RestaurantReservationDetailView(generics.RetrieveAPIView):
    serializer_class = ReservationSerializer
    lookup_url_kwarg = 'reserve_pk'

    def get_queryset(self):
        pk = self.kwargs['pk']
        restaurant = get_object_or_404(Restaurant, pk=pk)
        queryset = Reservation.objects.filter(restaurant=restaurant)
        return queryset


class CustomerReservationByDateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            start_year = self.request.data['start_year']
            start_month = self.request.data['start_month']
            start_day = self.request.data['start_day']
            end_year = self.request.data['end_year']
            end_month = self.request.data['end_month']
            end_day = self.request.data['end_day']
        except MultiValueDictKeyError:
            raise exceptions.ValidationError
        info = Reservation.objects.filter(
            information__date__range=[f'{start_year}-{start_month}-{start_day}',
                                      f'{end_year}-{end_month}-{end_day}'])
        filtered_info = info.filter(user=request.user)
        serializer = ReservationSerializer(filtered_info, many=True)
        return Response(serializer.data)
