from django.conf.urls import url

from reservations.views import PaymentList, test

urlpatterns = [
    # 결제정보 url
    url(r'^payment/$', PaymentList.as_view(), name='payment'),

    # 결제 테스트용 url
    url(r'^test/$', test)
]
