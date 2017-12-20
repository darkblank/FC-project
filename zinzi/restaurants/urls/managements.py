from django.conf.urls import url

from ..views import ManagementRestaurantView, CreateRestaurantImageView, UpdateDestroyRestaurantImageView, \
    CreateRestaurantMenuView, UpdateDestroyRestaurantMenuView

urlpatterns = [
    # /restaurants/<pk(restaurant pk)>/management/
    url(r'^(?P<pk>\d+)/$', ManagementRestaurantView.as_view(), name='management-restaurant'),

    # Management Restaurant Image

    # /restaurants/management/<pk(restaurant pk)>/image/
    url(r'^(?P<pk>\d+)/image/$', CreateRestaurantImageView.as_view(), name='create-restaurant-image'),
    # /restaurants/management/image/<pk(image pk)>/
    url(r'^image/(?P<pk>\d+)/$', UpdateDestroyRestaurantImageView.as_view(), name='update-destroy-image'),

    # Management Restaurant Menu Image

    # /restaurants/management/<pk(restaurant pk)>/menu/
    url(r'^(?P<pk>\d+)/menu/$', CreateRestaurantMenuView.as_view(), name='create-restaurant-menu'),
    # /restauratns/management/menu/<pk(menu pk)>/
    url(r'^menu/(?P<pk>\d+)/$', UpdateDestroyRestaurantMenuView.as_view(), name='update-destroy-menu'),
]
