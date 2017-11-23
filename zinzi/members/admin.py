from django.contrib import admin
from django.contrib.auth import get_user_model

from members.models import ExtraUserInfo, Preference

User = get_user_model()


class ExtraUSerInfoInline(admin.StackedInline):
    model = ExtraUserInfo


class UserAdmin(admin.ModelAdmin):
    inlines = (ExtraUSerInfoInline,)
    list_display = ('email', 'user_type', 'nickname', 'is_owner')

    def user_type(self, user):
        return user.extrauserinfo.user_type

    def nickname(self, user):
        return user.extrauserinfo.nickname

    def is_owner(self, user):
        return user.extrauserinfo.is_owner


admin.site.register(User, UserAdmin)
admin.site.register(Preference)
