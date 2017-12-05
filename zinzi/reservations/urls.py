from django.conf.urls import url

from reservations.views import PaymentCreateView, test

urlpatterns = [
    # 결제정보 url
    url(r'^payment/$', PaymentCreateView.as_view(), name='payment'),

    # 결제 테스트용 url
    url(r'^test/$', test)
]
