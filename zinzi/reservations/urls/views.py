from django.conf.urls import url

from reservations.views.payment import payment_view, payment_reservations_save_view, payment_complete_view, \
    payment_cancel_request_view, payment_cancel_confirm_view
from reservations.views.reservations import reservation_view, reservation_check_view, reservation_check_detail_view

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', reservation_view, name='reservation'),

    url(r'^payment/$', payment_view, name='payment'),
    url(r'^payment/save/$', payment_reservations_save_view, name='save_all'),
    url(r'^payment/complete/$', payment_complete_view, name='complete'),

    url(r'^paymentcancel/(?P<pk>\d+)/$', payment_cancel_request_view, name='payment_cancel'),
    url(r'^paymentcancel/confirm/(?P<pk>\d+)/$', payment_cancel_confirm_view, name='payment_cancel_confirm'),

    url(r'^check/$', reservation_check_view, name='reservation_check'),
    url(r'^check/(?P<pk>\d+)/$', reservation_check_detail_view, name='reservation_check_detail'),
]
