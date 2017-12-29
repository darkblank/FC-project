from django.conf.urls import include, url

from reservations.urls import apis
from reservations.urls import views

urlpatterns = [
    url(r'^', include(apis)),
    url(r'^views/', include(views, namespace='views')),
    ]