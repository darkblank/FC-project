from django.conf.urls import url

from .views import RestaurantListView, RestaurantDetailView

urlpatterns = [
    # /restaurants/
    url(r'^$', RestaurantListView.as_view(), name='restaurant-list'),
    # /restaurants/<pk>/
    url(r'(?P<pk>\d+)/$', RestaurantDetailView.as_view(), name='restaurant-detail'),
]
