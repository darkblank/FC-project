from django.contrib.auth import get_user_model
from django.shortcuts import render

from accounts.forms import UpdateProfileForm
from accounts.models import Profile

User = get_user_model()


def profile(request):
    target_user = Profile.objects.get(user=request.user)
    context = {
        'target_user': target_user,
    }
    return render(request, 'accounts/profile.html', context)


def update_profile(request, pk):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            nickname = request.POST['nickname']
            profile_image = request.POST['profile_image']
            Profile.objects.update(
                nickname=nickname,
                profile_image=profile_image,
            )
    else:
        form = UpdateProfileForm
    context = {
        'form': form,
    }
    return render(request, 'accounts/update_profile.html', context)
