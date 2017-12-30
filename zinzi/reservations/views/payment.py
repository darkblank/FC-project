from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from iamport import Iamport
from rest_framework import exceptions
from rest_framework.views import APIView

from reservations.models import Reservation
from reservations.serializers.payments import PaymentSerializer
from restaurants.models import ReservationInfo, Restaurant

User = get_user_model()


def payment_view(request):
    if request.method == 'POST':
        restaurant = request.POST.get('restaurant')
        information = request.POST.get('information')
        information_pk = request.POST.get('information_pk')
        name = request.POST.get('name')
        party = request.POST.get('party')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        price = request.POST.get('price')
        context = {
            'restaurant': restaurant,
            'information': information,
            'name': name,
            'party': party,
            'phone_number': phone_number,
            'email': email,
            'price': price,
            'information_pk': information_pk,
        }
        return render(request, 'reservation/payment.html', context)
    else:
        return Http404


class PaymentReservationsSaveView(APIView):
    def post(self, request):
        restaurant = request.data.get('restaurant')
        information = int(request.data.get('information'))
        name = request.data.get('name')
        party = int(request.data.get('party'))
        phone_number = int(request.data.get('phone_number'))
        email = request.data.get('email')
        price = int(request.data.get('price'))
        reservation = Reservation.objects.create(
            user=User.objects.first(),
            information=get_object_or_404(ReservationInfo, pk=information),
            restaurant=get_object_or_404(Restaurant, name=restaurant),
            name=name,
            party=party,
            phone_number=phone_number,
            email=email,
            price=price,
        )
        iamport = Iamport(imp_key=settings.IMP_KEY,
                          imp_secret=settings.IMP_SECRET)
        # 입력한 imp_uid로부터 결제정보를 가져옴
        payment = iamport.find(imp_uid=request.data.get('imp_uid'))
        # 주문 해야할 금액과 실제 결제 금액이 일치하는지 검증 후 일치하지 않으면 자동으로 취소
        # 취소 되었을 경우에는 취소 되어진 결제정보로 데이터베이스에 저장
        # 또한, 취소 되었을 경우 취소되었다는 메일 보냄(celery로 비동기 처리, celery config dev로 바꾸고 배포 관련 처리 하고 주석 빼야 함)
        if not iamport.is_paid(int(request.data.get('price')), imp_uid=request.data.get('imp_uid')):
            cancel = iamport.cancel(u'가격 불일치', imp_uid=request.data.get('imp_uid'))
            # send_mail_task.delay('Test', 'Test', 'darkblank1990@gmail.com')
            serializer = PaymentSerializer(data=cancel)
        else:
            serializer = PaymentSerializer(data=payment)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save(reservation=reservation)
            except IntegrityError:
                raise exceptions.ValidationError
            return HttpResponse('success')
        return HttpResponse('failed')
