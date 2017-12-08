from django.conf.urls import url

from reservations.views import PaymentCreateView, test, PaymentDetailUpdateView, \
    ReservationCreateView, CustomerReservationListView

urlpatterns = [
    # 예약정보 url
    url(r'^(?P<pk>\d+)/reservation/$', ReservationCreateView.as_view(), name='reservation-create'),
    url(r'^customer/$', CustomerReservationListView.as_view(), name='customer-reservation-list'),

    # 결제정보 url
    url(r'^payment/$', PaymentCreateView.as_view(), name='payment'),
    url(r'^(?P<imp_uid>imp_\d+)/payment/$', PaymentDetailUpdateView.as_view(), name='payment-detailupdate'),

    # 결제 테스트용 url
    url(r'^test/$', test)
]
