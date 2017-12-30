from django.conf.urls import url

from reservations.views.payment import payment_view, PaymentReservationsSaveView
from reservations.views.reservations import reservation_view

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', reservation_view, name='reservation'),

    url(r'^payment/$', payment_view, name='payment'),
    url(r'^payment/complete/$', PaymentReservationsSaveView.as_view(), name='save_all'),
]
