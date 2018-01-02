from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from restaurants.models import Restaurant, ReservationInfo


def restaurant_list_view(request):
    if request.method == "GET":
        q = request.GET.get('q', None)
        if q:
            restaurant = Restaurant.get_searched_list(q=q)
            return render(request, 'restaurant/list.html', {'list': restaurant})

        filter_fileds = {
            'restaurant_type': request.GET.get('type', None),
            'average_price': request.GET.get('price', None),
            'district': request.GET.get('district', None),
        }
        restaurant = Restaurant.get_filtered_list(filter_fields=filter_fileds)
        return render(request, 'restaurant/list.html', {'list': restaurant})
    else:
        raise Http404


def restaurant_detail_view(request, pk):
    if request.method == "GET":
        restaurant = get_object_or_404(Restaurant, pk=pk)
        return render(request, 'restaurant/detail.html', {'rest': restaurant})
    else:
        raise Http404


# def check_opened_time_view(request, pk):
#     res_pk = pk
#     date = request.GET.get('date', None)
#     queryset = ReservationInfo.check_acceptable_time(res_pk=res_pk, date=date)
#     if queryset is None:
#         raise ValidationError('party 또는 date가 정상적으로 입력되지 않았습니다.')
#     if not queryset.count():
#         raise ValidationError('예약 가능한 정보가 없습니다.')
#     return render(request, 'restaurant/check_opened_time.html', {'list': queryset})

