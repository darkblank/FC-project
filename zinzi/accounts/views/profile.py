from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import UpdateProfileForm
from accounts.models import Profile

User = get_user_model()


def profile(request):
    target_user = Profile.objects.get(user=request.user)
    context = {
        'target_user': target_user,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UpdateProfileForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/update_profile.html', context)
