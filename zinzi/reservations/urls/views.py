from django.conf.urls import url

from reservations.views.reservations import reservation_view

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', reservation_view, name='reservation'),
]
