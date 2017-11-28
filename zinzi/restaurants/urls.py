from django.conf.urls import url

from .views import RestaurantListView

urlpatterns = [
    # /restaurants/list/
    url(r'^list/$', RestaurantListView.as_view(), name='list'),
    # /restaurants/<pk>/
    # url(r'^(?P<rst_pk>\d+)/$', ),
]
