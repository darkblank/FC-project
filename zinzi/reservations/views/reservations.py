from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from reservations.forms import ReservationForm
from reservations.models import Reservation, Payment
from restaurants.models import Restaurant, ReservationInfo


@login_required
def reservation_view(request, pk):
    if request.is_ajax():
        info_pk = request.GET.get('info')
        info = get_object_or_404(ReservationInfo, pk=info_pk)
        data = {
            "max_party": info.acceptable_size_of_party,
        }
        return JsonResponse(data)
    if request.method == 'GET':
        date = request.GET.get('date')
        restaurant = Restaurant.objects.get(pk=pk)
        form = ReservationForm(restaurant, date)
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


# 유저 프로필쪽에 추가 요청(부기형한테)
@login_required()
def reservation_check_view(request):
    if request.user.profile.is_owner:
        restaurant = get_object_or_404(Restaurant, owner=request.user)
        reservations = Reservation.objects.filter(restaurant=restaurant).order_by('information__date')

    else:
        reservations = Reservation.objects.filter(user=request.user).order_by('information__date')
    context = {
        'reservations': reservations,
    }
    return render(request, 'reservation/reservation_check.html', context)


@login_required()
def reservation_check_detail_view(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    payment = get_object_or_404(Payment, reservation=reservation)
    context = {
        'reservation': reservation,
        'payment': payment,
    }
    return render(request, 'reservation/reservation_check_detail.html', context)
