from django.conf.urls import url

# from ..apis import RestaurantDetailView, CheckOpenedTimeView, CommentListCreateView
from restaurants.views.restaurants import restaurant_detail_view

urlpatterns = [
    # /restaurants/<pk>/
    url(r'^$', restaurant_detail_view, name='restaurant-detail'),
    # # /restaurants/<pk>/check_opened_time/?party=<int>&date=<date(YYYY-MM-DD)>
    # url(r'^check_opened_time/$', CheckOpenedTimeView.as_view(), name='check-time'),
    # # /restaurants/<pk(comment pk)>/comments/
    # url(r'^comments/$', CommentListCreateView.as_view(), name='comment-list-create'),
]
