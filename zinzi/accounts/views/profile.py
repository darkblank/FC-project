from django.contrib.auth import get_user_model
from django.shortcuts import render

from accounts.models import Profile

User = get_user_model()


def profile(request, pk):
    target_user = Profile.objects.get(pk=pk)
    context = {
        'target_user': target_user,
    }
    return render(request, 'accounts/profile.html', context)
