from django.shortcuts import render

from reservations.forms import ReservationForm
from restaurants.models import Restaurant


def reservation_view(request, pk):
    # method POST로 변경 해야 함(지현님 url 추가 뒤)
    if request.method == 'GET':
        restaurant = Restaurant.objects.get(pk=pk)
        form = ReservationForm()
        context = {
            'restaurant': restaurant,
            'form': form,
        }
        return render(request, 'reservation/reservation.html', context)
