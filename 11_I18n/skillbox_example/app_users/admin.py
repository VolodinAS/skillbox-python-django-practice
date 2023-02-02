from django.contrib import admin

from app_users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']


admin.site.register(User, UserAdmin)
