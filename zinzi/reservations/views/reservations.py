from django.shortcuts import render

from reservations.forms import ReservationForm
from restaurants.models import Restaurant


def reservation_view(request, pk):
    # 지현님 레스토랑 디테일 뷰에서 예약하기 버튼 누를시 리다이렉트 이쪽으로
    if request.method == 'GET':
        restaurant = Restaurant.objects.get(pk=pk)
        form = ReservationForm()
        context = {
            'restaurant': restaurant,
            'form': form,
        }
        return render(request, 'reservation/reservation.html', context)
