from django.conf.urls import url

from reservations.views.payment import payment_view, payment_reservations_save_view, payment_complete_view
from reservations.views.reservations import reservation_view, customer_reservation_check_view

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', reservation_view, name='reservation'),

    url(r'^payment/$', payment_view, name='payment'),
    url(r'^payment/save/$', payment_reservations_save_view, name='save_all'),
    url(r'^payment/complete/$', payment_complete_view, name='complete'),

    url(r'^customer/check/$', customer_reservation_check_view, name='customer_reservation'),
]
