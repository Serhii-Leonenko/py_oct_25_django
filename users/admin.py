from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_select_related = ("user",)
