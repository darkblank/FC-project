from django.conf.urls import url

from restaurants.views.managements import CreateRestaurantMenuView, UpdateDestroyRestaurantMenuView
from .views import RestaurantListView, RestaurantDetailView, CheckOpenedTimeView, CommentListCreateView, \
    CommentUpdateDestroyView, ManagementRestaurantView, CreateRestaurantImageView, UpdateDestroyRestaurantImageView

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
    url(r'^management/(?P<pk>\d+)/$', ManagementRestaurantView.as_view(), name='management-restaurant'),

    # Management Restaurant Image

    # /restaurants/management/<pk(restaurant pk)>/image/
    url(r'^management/(?P<pk>\d+)/image/$', CreateRestaurantImageView.as_view(), name='create-restaurant-image'),
    # /restaurants/management/image/<pk(image pk)>/
    url(r'^management/image/(?P<pk>\d+)/$', UpdateDestroyRestaurantImageView.as_view(), name='update-destroy-image'),

    # Management Restaurant Menu Image

    # /restaurants/management/<pk(restaurant pk)>/menu/
    url(r'^management/(?P<pk>\d+)/menu/$', CreateRestaurantMenuView.as_view(), name='create-restaurant-menu'),
    # /restauratns/management/menu/<pk(menu pk)>/
    url(r'^management/menu/(?P<pk>\d+)/$', UpdateDestroyRestaurantMenuView.as_view(), name='update-destroy-menu'),
]
