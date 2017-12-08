from django.conf.urls import url

from .views import RestaurantListView, RestaurantDetailView, CheckOpenedTimeView, CommentListCreateView, \
    CommentUpdateDestroyView

urlpatterns = [
    # /restaurants/
    url(r'^$', RestaurantListView.as_view(), name='restaurant-list'),
    # /restaurants/<pk>/
    url(r'(?P<pk>\d+)/$', RestaurantDetailView.as_view(), name='restaurant-detail'),
    url(r'(?P<pk>\d+)/check_opened_time/$', CheckOpenedTimeView.as_view(), name='check-time'),
    url(r'(?P<pk>\d+)/comments/$', CommentListCreateView.as_view(), name='comment-list-create'),
    url(r'comments/(?P<pk>\d+)/$', CommentUpdateDestroyView.as_view(), name='comment-update-destroy'),
]
