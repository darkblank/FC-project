from django.conf.urls import url

from reservations.views.payment import payment_view, payment_reservations_save_view
from reservations.views.reservations import reservation_view

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', reservation_view, name='reservation'),

    url(r'^payment/$', payment_view, name='payment'),
    url(r'^payment/save/$', payment_reservations_save_view, name='save_all'),
]
