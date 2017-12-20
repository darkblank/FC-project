from django.conf.urls import url

from .views import RestaurantListView, RestaurantDetailView, CheckOpenedTimeView, CommentListCreateView, \
    CommentUpdateDestroyView, ManagementRestaurantView

urlpatterns = [
    # Restaurants

    # /restaurants/
    url(r'^$', RestaurantListView.as_view(), name='restaurant-list'),
    # /restaurants/<pk>/
    url(r'^(?P<pk>\d+)/$', RestaurantDetailView.as_view(), name='restaurant-detail'),
    # /restaurants/<pk>/check_opened_time/?party=<int>&date=<date(YYYY-MM-DD)>
    url(r'^(?P<pk>\d+)/check_opened_time/$', CheckOpenedTimeView.as_view(), name='check-time'),
    # /restaurants/<pk(comment pk)>/comments/
    url(r'^(?P<pk>\d+)/comments/$', CommentListCreateView.as_view(), name='comment-list-create'),

    # Comment

    # /restaurants/comments/<pk(comment pk)>/
    url(r'^comments/(?P<pk>\d+)/$', CommentUpdateDestroyView.as_view(), name='comment-update-destroy'),

    # Management

    # /restaurants/<pk(restaurant pk)>/management/
    url(r'^(?P<pk>\d+)/management/$', ManagementRestaurantView.as_view(), name='management-restaurant'),
]
