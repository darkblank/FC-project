from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from reservations.forms import ReservationForm
from reservations.models import Reservation, Payment
from restaurants.models import Restaurant, ReservationInfo


@login_required
def reservation_view(request, pk):
    # 지현님 레스토랑 디테일 뷰에서 예약하기 버튼 누를시 리다이렉트 이쪽으로
    if request.method == 'GET':
        restaurant = Restaurant.objects.get(pk=pk)
        form = ReservationForm(restaurant)
        context = {
            'restaurant': restaurant,
            'form': form,
        }
        return render(request, 'reservation/reservation.html', context)
    else:
        restaurant = Restaurant.objects.get(pk=pk)
        information_pk = request.POST.get('information')
        information = get_object_or_404(ReservationInfo, pk=information_pk)
        name = request.POST.get('name')
        party = int(request.POST.get('party'))
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        price = information.price * party
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
        return render(request, 'reservation/check.html', context)


# 고객 프로필 페이지 쪽에 url 추가(부기형한테)
@login_required()
def customer_reservation_check_view(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('information__date')
    context = {
        'reservations': reservations,
    }
    return render(request, 'reservation/customer_reservation.html', context)


@login_required()
def customer_reservation_check_detail_view(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    context = {
        'reservation': reservation,
    }
    return render(request, 'reservation/customer_reservation_detail.html', context)


@login_required()
def owner_reservation_check_view(request):
    # 오우너 프로필 페이지 쪽에 url 추가(부기형)
    # 현재 로그인 유저가 레스토랑의 owner일 경우에만 접근 가능(owner가 아닐경우 404)
    if request.user.profile.is_owner:
        restaurant = get_object_or_404(Restaurant, owner=request.user)
        reservations = Reservation.objects.filter(restaurant=restaurant)
        context = {
            'reservations': reservations,
        }
        return render(request, 'reservation/owner_reservation.html', context)
    raise Http404


@login_required()
def owner_reservation_check_detail_view(request, pk):
    if request.user.profile.is_owner:
        reservation = get_object_or_404(Reservation, pk=pk)
        payment = get_object_or_404(Payment, reservation=reservation)
        context = {
            'reservation': reservation,
            'payment': payment,
        }
        return render(request, 'reservation/owner_reservation_detail.html', context)
    raise Http404
