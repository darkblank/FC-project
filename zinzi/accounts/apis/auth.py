import requests
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status, mixins, generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import NamedTuple

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
    'FacebookLoginView',
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


# 페이스북 로그인
class FacebookLoginView(APIView):
    def post(self, request):
        # Debug결과의 NamedTuple
        class DebugTokenInfo(NamedTuple):
            app_id: str
            application: str
            expires_at: int
            is_valid: bool
            scopes: list
            type: str
            user_id: str

        # token(access_token)을 받아 해당 토큰을 Debug
        def get_debug_token_info(token):
            app_id = settings.FACEBOOK_APP_ID
            app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
            app_access_token = f'{app_id}|{app_secret_code}'

            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': token,
                'access_token': app_access_token,
            }
            response = requests.get(url_debug_token, params_debug_token)
            return DebugTokenInfo(**response.json()['data'])

        # request.data로 전달된 access_token값을 페이스북API쪽에 debug요청, 결과를 받아옴
        debug_token_info = get_debug_token_info(request.data['access_token'])

        if debug_token_info.user_id != request.data['facebook_user_id']:
            raise APIException('페이스북 토큰의 사용자와 전달받은 facebook_user_id가 일치하지 않음')

        if not debug_token_info.is_valid:
            raise APIException('페이스북 토큰이 유효하지 않음')

        user = authenticate(facebook_user_id=request.data['facebook_user_id'])
        if not user:
            user = User.objects.create_user(
                username=f'fb_{request.data["facebook_user_id"]}',
                user_type=User.USER_TYPE_FACEBOOK,
            )
        data = {
            'user': UserSerializer(user).data,
            'token': user.token,
        }
        return Response(data)