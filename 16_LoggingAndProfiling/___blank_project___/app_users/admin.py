from django.contrib import admin

from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Админка профиля
    """
    list_display = [
        'id',
        'user',
        'balance'
    ]


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    """
    Админка статусов
    """
    list_display = [
        'id',
        'title',
        'expenses_lt'
    ]
