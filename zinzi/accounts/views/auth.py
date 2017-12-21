from django.contrib.auth import get_user_model, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status, mixins, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import SignupSerializer, UserSerializer, ChangePasswordSerializer
from utils.permissions import IsUserOrNotAllow

User = get_user_model()

__all__ = (
    'SignupView',
    'SigninView',
    'SignoutView',
    'ChangePasswordView',
    'ResetPasswordView',
    'WithdrawView',
)


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
            email = EmailMultiAlternatives(
                mail_subject,
                html_message,
                to=[to_email],
            )
            email.attach_alternative(html_message, 'text/html')
            email.send()
            data = {
                'user': serializer.data
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = (
        IsUserOrNotAllow,
    )

    def post(self, request):
        request.user.auth_token.delete()
        data = {
            'message': 'Successfully logged out.'
        }
        return Response(data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (
        IsUserOrNotAllow,
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


# 회원탈퇴 기능
class WithdrawView(mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    serializer_class = UserSerializer
    model = User
    permission_classes = (
        IsUserOrNotAllow,
    )

    def get_object(self):
        obj = self.request.user
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
