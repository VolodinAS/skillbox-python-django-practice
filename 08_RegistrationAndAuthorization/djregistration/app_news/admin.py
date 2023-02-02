from django.contrib import admin

from .models import NewsItem


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'header',
        'create_at',
        'updated_at',
        'user',
        'published',
        'publicised_at',
        'published_by',
        'tag'
    ]
    # pass
