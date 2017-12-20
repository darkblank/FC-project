from django.conf.urls import url, include

from . import managements, detail
from ..views import RestaurantListView, CommentUpdateDestroyView

urlpatterns = [
    # /restaurant/<pk(restaurant pk)>/
    url(r'^(?P<pk>\d+)/', include(detail, namespace='detail')),
    # /restaurant/management/
    url(r'^management/', include(managements, namespace='management')),
    # /restaurants/
    url(r'^$', RestaurantListView.as_view(), name='restaurant-list'),
    # /restaurants/<pk>/
    # /restaurants/comments/<pk(comment pk)>/
    url(r'^comments/(?P<pk>\d+)/$', CommentUpdateDestroyView.as_view(), name='comment-update-destroy'),
    # Management

]
