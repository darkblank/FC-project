from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import SignupSerializer, UserSerializer, ProfileSerializer, PreferenceSerializer

User = get_user_model()


class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # 이메일 인증을 할 시 True로 바뀜 (현재 기본값은 True)
            user.is_active = True
            user.save()
            # current_site = get_current_site(request)
            # mail_subject = '[Zinzi] 이메일 인증'
            # message = render_to_string('<activation.html>', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # to_email = serializer.validated_data['email']
            # email = EmailMessage(
            #     mail_subject,
            #     message,
            #     to=[to_email],
            # )
            # email.send()
            Profile.objects.create(user=user)
            data = {
                'user': serializer.data,
            }
            return Response(data=data, status=status.HTTP_201_CREATED)


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

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


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
