from django.contrib import admin

from app_author.models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'last_name',
        'first_name',
        'birthday'
    ]
