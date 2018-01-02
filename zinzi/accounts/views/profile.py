from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import UpdateProfileForm
from accounts.models import Profile
from restaurants.models import Restaurant

User = get_user_model()


@login_required
def profile(request):
    if request.user.is_authenticated:
        target_user = Profile.objects.get(user=request.user)
        restaurants = Restaurant.objects.get(owner=request.user)
        context = {
            'target_user': target_user,
            'restaurants': restaurants,
        }
        return render(request, 'accounts/profile.html', context)
    return redirect('accounts:signin')


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
