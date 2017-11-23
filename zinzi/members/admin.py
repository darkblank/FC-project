from django.contrib import admin
from django.contrib.auth import get_user_model

from members.models import ExtraUserInfo, Preference

User = get_user_model()

admin.site.register(User)
admin.site.register(ExtraUserInfo)
admin.site.register(Preference)
