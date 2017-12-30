from django.conf.urls import url

from reservations.views.payment import payment_view
from reservations.views.reservations import reservation_view

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', reservation_view, name='reservation'),
    url(r'^payment/$', payment_view, name='payment'),
]
