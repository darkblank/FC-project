from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions

from reservations.models import Reservation
from reservations.serializers import ReservationSerializer
from restaurants.models import ReservationInfo, Restaurant
from utils.permissions import IsUserOrNotAllow

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
    permission_classes = (IsUserOrNotAllow,)


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
