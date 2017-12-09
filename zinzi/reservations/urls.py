from django.conf.urls import url

from reservations.views import PaymentCreateView, test, PaymentDetailUpdateView, \
    ReservationCreateView, CustomerReservationListView, CustomerReservationDetailView, RestaurantReservationListView, \
    RestaurantReservationDetailView

urlpatterns = [
    # 예약정보 url
    url(r'^(?P<pk>\d+)/reservation/$', ReservationCreateView.as_view(), name='reservation-create'),

    url(r'^customer/$', CustomerReservationListView.as_view(), name='customer-reservation-list'),
    url(r'^(?P<pk>\d+)/customer/$', CustomerReservationDetailView.as_view(), name='customer-reservation-detail'),

    url(r'^(?P<pk>\d+)/restaurant/$', RestaurantReservationListView.as_view(), name='restaurant-reservation-list'),
    url(r'^(?P<pk>\d+)/restaurant/(?P<reserve_pk>\d+)/$',
        RestaurantReservationDetailView.as_view(),
        name='restaurant-reservation-detail'),

    # 결제정보 url
    url(r'^(?P<pk>\d+)/payment/$', PaymentCreateView.as_view(), name='payment'),
    url(r'^(?P<imp_uid>imp_\d+)/payment/$', PaymentDetailUpdateView.as_view(), name='payment-detailupdate'),

    # 결제 테스트용 url
    url(r'^test/$', test)
]
