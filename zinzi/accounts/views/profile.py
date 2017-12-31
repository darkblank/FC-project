from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import Profile

User = get_user_model()


def profile(request):
    target_user = Profile.objects.get(user=request.user)
    context = {
        'target_user': target_user,
    }
    return render(request, 'accounts/profile.html', context)


def update_profile(request, pk):
    return HttpResponse('폼 만들어야함...')
