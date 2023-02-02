from django.contrib import admin

from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'balance'
    ]


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'expenses_lt'
    ]
