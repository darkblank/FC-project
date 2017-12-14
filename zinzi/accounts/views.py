from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.tokens import account_activation_token
from .models import Profile
from .serializers import SignupSerializer, UserSerializer, ProfileSerializer, PreferenceSerializer, \
    ChangePasswordSerializer

User = get_user_model()


class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # 이메일 인증을 할 시 True로 바뀜 (현재 기본값은 True)
            user = serializer.data
            current_site = get_current_site(request)
            mail_subject = '[Zinzi] 이메일 인증'
            message = render_to_string('activation.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = serializer.validated_data['email']
            email = EmailMessage(
                mail_subject,
                message,
                to=[to_email],
            )
            email.send()
            data = {
                'user': serializer.data,
            }
            return Response(data=data, status=status.HTTP_201_CREATED)


class Activation(APIView):
    def get(self, request, uidb64, token):
        uid = force_text(urlsafe_base64_decode(uidb64))
        decode_token = force_text(urlsafe_base64_decode(token))
        user = User.objects.get(pk=uid)

        if decode_token == request.user.token:
            user.is_active = True
            user.save()
            Profile.objects.create(user=user)
            data = {
                'token': token,
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Signin(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(
            email=email,
            password=password,
        )

        if user:
            token, token_created = Token.objects.get_or_create(user=user)
            data = {
                'user': UserSerializer(user).data,
                'token': token.key,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'email': email,
                'password': password,
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class Signout(APIView):
    queryset = User.objects.all()

    def post(self, request):
        request.user.auth_token.delete()
        data = {
            'message': 'Successfully logged out.'
        }
        return Response(data, status=status.HTTP_200_OK)


class ProfileUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'user'
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )


class PreferenceUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = PreferenceSerializer
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'user',
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not serializer.validated_data['new_password'] == serializer.validated_data['new_password_confirm']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if serializer.validated_data['old_password'] == serializer.validated_data['new_password']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(APIView):
    pass
