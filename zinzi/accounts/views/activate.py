from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.authtoken.models import Token

from accounts.models import Profile
from accounts.serializers import UserSerializer

User = get_user_model()

__all__ = (
    'activate',
)


def activate(self, uidb64, token):
    uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
    token = force_text(urlsafe_base64_decode(self.kwargs['token']))

    user = User.objects.get(pk=uid)

    if token == Token.objects.get(user=user).key:
        user.is_active = True
        user.save()
        Profile.objects.create(user=user)
        data = {
            'token': token,
            'user': UserSerializer(user).data
        }
        return redirect(data, 'http://localhost:8000/accounts/signin/')
    return redirect('http://localhost:8000/accounts/signup/')
