from django.conf.urls import url

from reservations.views import test
from reservations.views.favorites import RestaurantFavoriteToggle, CustomerFavoriteListView
from reservations.views.payments import PaymentCreateView, PaymentDetailUpdateView, PaymentCancelCreateDetailView, \
    PaymentListView
from reservations.views.reservations import ReservationCreateView, ReservationPatchView, CustomerReservationListView, \
    CustomerReservationDetailView, RestaurantReservationListView, RestaurantReservationDetailView, \
    RestaurantReservationByDate

urlpatterns = [
    # 예약정보 url
    url(r'^(?P<pk>\d+)/reservation/$', ReservationCreateView.as_view(), name='reservation-create'),
    url(r'^(?P<pk>\d+)/reservation/addinfo/$', ReservationPatchView.as_view(), name='reservation-patch'),

    url(r'^customer/$', CustomerReservationListView.as_view(), name='customer-reservation-list'),
    url(r'^(?P<pk>\d+)/customer/$', CustomerReservationDetailView.as_view(), name='customer-reservation-detail'),

    url(r'^(?P<pk>\d+)/restaurant/$', RestaurantReservationListView.as_view(), name='restaurant-reservation-list'),
    url(r'^(?P<pk>\d+)/restaurant/(?P<reserve_pk>\d+)/$',
        RestaurantReservationDetailView.as_view(),
        name='restaurant-reservation-detail'),

    url(r'^date/$', RestaurantReservationByDate.as_view(),),

    # 결제정보 url
    url(r'^(?P<pk>\d+)/payment/$', PaymentCreateView.as_view(), name='payment-create'),
    url(r'^payment/$', PaymentListView.as_view(), name='payment-list'),
    url(r'^(?P<imp_uid>imp_\d+)/payment/$', PaymentDetailUpdateView.as_view(), name='payment-detailupdate'),

    url(r'^(?P<imp_uid>imp_\d+)/paymentcancel/$', PaymentCancelCreateDetailView.as_view(),
        name='paymentcancel-createdetail'),

    # 즐겨찾기
    url(r'^(?P<pk>\d+)/favorite-toggle/$', RestaurantFavoriteToggle.as_view(), name='favorite-toggle'),

    url(r'^favorite-toggle/$', CustomerFavoriteListView.as_view(), name='customer-favorite'),

    # 결제 테스트용 url
    url(r'^test/$', test)
]
