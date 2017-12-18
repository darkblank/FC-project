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

from .models import Profile
from .serializers import SignupSerializer, UserSerializer, ProfileSerializer, PreferenceSerializer, \
    ChangePasswordSerializer

User = get_user_model()


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # 이메일 인증 전까진 is_active = False (테스트를 위해 True로 임시 설정)
            user.is_active = True
            user.save()
            # 이메일 인증 메시지 보내기
            current_site = get_current_site(request)
            mail_subject = '[Zinzi] 이메일 인증'
            html_message = render_to_string('user_activate.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': urlsafe_base64_encode(force_bytes(user.token)),
            })
            to_email = serializer.validated_data['email']
            email = EmailMessage(
                mail_subject,
                html_message,
                to=[to_email],
            )
            email.send()
            data = {
                'user': serializer.data
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):
    def get(self, request, uidb64, token):
        uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
        decoded = force_text(urlsafe_base64_decode(token))

        user = User.objects.get(pk=uid)

        if decoded == Token.objects.get(user=user).key:
            user.is_active = True
            user.save()
            Profile.objects.create(user=user)
            data = {
                'token': token,
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
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


class SignoutView(APIView):
    queryset = User.objects.all()

    def post(self, request):
        request.user.auth_token.delete()
        data = {
            'message': 'Successfully logged out.'
        }
        return Response(data, status=status.HTTP_200_OK)


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'user'
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )


class UpdatePreferenceView(generics.RetrieveUpdateAPIView):
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


class ResetPasswordView(APIView):
    pass
