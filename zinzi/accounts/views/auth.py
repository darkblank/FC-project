from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status, mixins, generics
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.forms import SignupForm, SigninForm
from accounts.serializers import UserSerializer, ChangePasswordSerializer
from utils.permissions import IsUserOrNotAllow

User = get_user_model()

__all__ = (
    'signup',
    'signin',
    'signout',
    'withdraw',
)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # 이메일 인증 메시지 보내기
            current_site = get_current_site(request)
            mail_subject = '[Zinzi] 이메일 인증'
            html_message = render_to_string('user_activate.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': urlsafe_base64_encode(force_bytes(user.token)),
            })
            to_email = form.cleaned_data['email']
            email = EmailMultiAlternatives(
                mail_subject,
                html_message,
                to=[to_email],
            )
            email.attach_alternative(html_message, 'text/html')
            email.send()
            return HttpResponse('이메일 인증을 위해 이메일을 확인해주십시오.')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(
                email=email,
                password=password,
            )
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('다시 시도해주십시오.')
    else:
        form = SigninForm
    context = {
        'form': form,
    }
    return render(request, 'accounts/signin.html', context)


def signout(request):
    logout(request)
    return redirect('index')


# 회원 비활성화 기능
@login_required
def withdraw(request):
    user = request.user
    user.is_active = False
    user.save()
    return redirect('index')


# 비밀번호 변경
# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.POST)
#         if form.is_valid():
#             user = User.objects.get(user=request.user)
#             password = form.cleaned_data['password1']
#             password_confirm = form.cleaned_data['password2']
#             if password == password_confirm:
#                 user.set_password(password)
#                 user.save()
#                 return redirect('accounts:profile')
#     else:
#         form = PasswordChangeForm
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/reset-password.html', context)


# 페이스북 로그인
def facebook_login(request):
    pass
