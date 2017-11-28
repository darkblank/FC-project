from django.conf.urls import url

from .views import RestaurantListView

urlpatterns = [
    # /restaurants/
    url(r'^$', RestaurantListView.as_view(), name='list'),
    # /restaurants/<pk>/
    # url(r'^(?P<rst_pk>\d+)/$', ),
]
