from django.conf.urls import url

from .views import RestaurantListView, RestaurantDetailView, CheckOpenedTimeView, CommentListView

urlpatterns = [
    # /restaurants/
    url(r'^$', RestaurantListView.as_view(), name='restaurant-list'),
    # /restaurants/<pk>/
    url(r'(?P<pk>\d+)/$', RestaurantDetailView.as_view(), name='restaurant-detail'),
    url(r'check_opened_time/$', CheckOpenedTimeView.as_view(), name='check-time'),
    url(r'(?P<res_pk>\d+)/comments/$', CommentListView.as_view(), name='comment-list'),
]
