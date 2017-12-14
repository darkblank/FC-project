from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^signin/$', views.SigninView.as_view(), name='signin'),
    url(r'^signout/$', views.SignoutView.as_view(), name='signout'),
    url(r'^(?P<pk>\d+)/profile/$', views.UpdateProfileView.as_view(), name='profile'),
    url(r'^(?P<pk>\d+)/change-password/$', views.ChangePasswordView.as_view(), name='change-password')
    # url(r'^(?P<pk>\d+)/preference/$', views.PreferenceUpdate.as_view(), name='preference')
    # url(r'(?P<user_pk>\d+)/my-reservation/$' ),
]
