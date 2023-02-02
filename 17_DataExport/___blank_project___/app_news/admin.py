from django.contrib import admin

from .models import *


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'published_at',
        'author',
        'is_published'
    ]
