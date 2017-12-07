from django.shortcuts import render
from iamport import Iamport
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Payment
from reservations.serializers import PaymentSerializer, ReservationSerializer
from restaurants.models import ReservationInfo


def test(request):
    return render(request, 'test.html')


class PaymentCreateView(APIView):
    def post(self, request):
        iamport = Iamport(imp_key='6343293486082258',
                          imp_secret='JEAB6oXOMsc2oysgdu4tJzlfgQvn5sfP7Qqefn21Qe3fNwv11zuL9Q0qGvNMY2B6T1l8pn9fCdvpK0rL')
        response = iamport.find(imp_uid=request.data.get('imp_uid'))
        serializer = PaymentSerializer(data=response)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'imp_uid'


# fix me
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
        )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
