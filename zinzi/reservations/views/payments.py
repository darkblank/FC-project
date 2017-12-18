from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from iamport import Iamport
from rest_framework import exceptions
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Reservation, Payment
from reservations.serializers.payments import PaymentSerializer, PaymentCancelSerializer
from reservations.tasks import send_mail_task

User = get_user_model()


# 가격 불일치시 메일이나 문자 보내주는 메서드도 추가 필요
# status==paid 인지 확인 필요
class PaymentCreateView(APIView):
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        iamport = Iamport(imp_key=settings.IMP_KEY,
                          imp_secret=settings.IMP_SECRET)
        # 입력한 imp_uid로부터 결제정보를 가져옴
        payment = iamport.find(imp_uid=request.data.get('imp_uid'))
        # 주문 해야할 금액과 실제 결제 금액이 일치하는지 검증 후 일치하지 않으면 자동으로 취소
        # 취소 되었을 경우에는 취소 되어진 결제정보로 데이터베이스에 저장
        # 또한, 취소 되었을 경우 취소되었다는 메일 보냄(celery로 비동기 처리)
        if not iamport.is_paid(int(request.data.get('price')), imp_uid=request.data.get('imp_uid')):
            cancel = iamport.cancel(u'가격 불일치', imp_uid=request.data.get('imp_uid'))
            send_mail_task.delay('Test', 'Test', 'darkblank1990@gmail.com')
            serializer = PaymentSerializer(data=cancel)
        else:
            serializer = PaymentSerializer(data=payment)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save(reservation=reservation)
            except IntegrityError:
                raise exceptions.ValidationError
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetailUpdateView(APIView):
    def patch(self, request, imp_uid):
        payment = get_object_or_404(Payment, imp_uid=imp_uid)
        iamport = Iamport(imp_key=settings.IMP_KEY,
                          imp_secret=settings.IMP_SECRET)
        # 입력한 취소 사유로 해당 imp_uid의 결제 취소 진행
        # Iamport.ResponseError > 이미 결제 취소되어진 경우
        try:
            cancel = iamport.cancel(request.data['reason'], imp_uid=payment.imp_uid)
        except Iamport.ResponseError:
            raise exceptions.NotAcceptable('Already cancelled')
        except MultiValueDictKeyError:
            raise exceptions.ValidationError
        serializer = PaymentSerializer(payment, data=cancel, partial=True)
        # 결제 취소가 이루어지면 해당 결제 정보에 연결된 예약 정보의 status 필드를 cancelled로 변경
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            payment.reservation.status = 'cancelled'
            payment.reservation.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, imp_uid):
        payment = get_object_or_404(Payment, imp_uid=imp_uid)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)


class PaymentCancelCreateDetailView(APIView):
    def post(self, request, imp_uid):
        payment = get_object_or_404(Payment, imp_uid=imp_uid)
        serializer = PaymentCancelSerializer(data=request.data)
        # 결제 취소 요청 정보를 입력하면 연결된 예약 정보의 status 필드를 request로 변경
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save(payment=payment)
                payment.reservation.status = 'request'
                payment.reservation.save()
            except IntegrityError:
                raise exceptions.ValidationError
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, imp_uid):
        payment = get_object_or_404(Payment, imp_uid=imp_uid)
        data = PaymentCancelSerializer(payment.paymentcancel).data
        return Response(data)
