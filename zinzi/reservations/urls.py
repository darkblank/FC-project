from django.conf.urls import url

from reservations.views import PaymentList

urlpatterns = [
    # url(r'^information/$', ),
    url(r'^payment/$', PaymentList.as_view(), name='payment'),
]
