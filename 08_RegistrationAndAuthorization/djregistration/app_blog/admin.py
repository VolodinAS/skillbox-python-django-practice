from django.contrib import admin

from app_blog.models import *


class BlogImagesTabularInline(admin.TabularInline):
    """
    Админка редактирования новости с привязкой комментов
    """
    model = BlogImages


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'header',
        'content',
        'create_at',
        'updated_at'
    ]
    inlines = [BlogImagesTabularInline]


@admin.register(BlogImages)
class BlogImagesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'blog',
        'image',
        'upload_at',
    ]
