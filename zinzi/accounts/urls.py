from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^signin/$', views.Signin.as_view(), name='signin'),
    url(r'^(?P<user_pk>\d+)/profile/$', views.Profile.as_view(), name='profile'),
    # url(r'(?P<user_pk>\d+)/my-reservation/$' ),
]
