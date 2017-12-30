from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from iamport import Iamport

from reservations.models import Reservation, Payment
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
        restaurant_pk = request.POST.get('restaurant_pk')
        context = {
            'restaurant': restaurant,
            'information': information,
            'name': name,
            'party': party,
            'phone_number': phone_number,
            'email': email,
            'price': price,
            'information_pk': information_pk,
            'restaurant_pk': restaurant_pk,
        }
        return render(request, 'reservation/payment.html', context)
    else:
        return Http404


def payment_reservations_save_view(request):
    if request.method == 'POST':
        restaurant = int(request.POST.get('restaurant'))
        information = int(request.POST.get('information'))
        name = request.POST.get('name')
        party = int(request.POST.get('party'))
        phone_number = int(request.POST.get('phone_number'))
        email = request.POST.get('email')
        price = int(request.POST.get('price'))
        # 유저 리퀘스트 유저로 바꿔줘야
        reservation = Reservation.objects.create(
            user=User.objects.first(),
            information=get_object_or_404(ReservationInfo, pk=information),
            restaurant=get_object_or_404(Restaurant, pk=restaurant),
            name=name,
            party=party,
            phone_number=phone_number,
            email=email,
            price=price,
        )
        iamport = Iamport(imp_key=settings.IMP_KEY,
                          imp_secret=settings.IMP_SECRET)
        # 입력한 imp_uid로부터 결제정보를 가져옴
        payment = iamport.find(imp_uid=request.POST.get('imp_uid'))
        # 주문 해야할 금액과 실제 결제 금액이 일치하는지 검증 후 일치하지 않으면 자동으로 취소
        # 취소 되었을 경우에는 취소 되어진 결제정보로 데이터베이스에 저장
        # 또한, 취소 되었을 경우 취소되었다는 메일 보냄(celery로 비동기 처리, celery config dev로 바꾸고 배포 관련 처리 하고 주석 빼야 함)
        all_fields = [f.name for f in Payment._meta.get_fields()]
        if not iamport.is_paid(int(request.POST.get('price')), imp_uid=request.POST.get('imp_uid')):
            cancel = iamport.cancel(u'가격 불일치', imp_uid=request.POST.get('imp_uid'))
            # send_mail_task.delay('Test', 'Test', 'darkblank1990@gmail.com')
            Payment.objects.create(
                **{key: value for key, value in cancel.items() if key in all_fields},
                reservation=reservation
            )
        else:
            Payment.objects.create(
                **{key: value for key, value in payment.items() if key in all_fields},
                reservation=reservation
            )
            return HttpResponse('success')
        return HttpResponse('failed')
