from django.contrib import admin

from .models_dir import Comment
from .models_dir import NewsItem


class CommentTabularInline(admin.TabularInline):
    """
    Админка редактирования новости с привязкой комментов
    """
    model = Comment


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    """
    Админка для списка новостей
    """
    
    actions = ['mark_as_enabled', 'mark_as_disabled']
    
    def mark_as_enabled(self, request, queryset):
        queryset.update(activity=True)
    
    def mark_as_disabled(self, request, queryset):
        queryset.update(activity=False)
    
    mark_as_enabled.short_description = 'Активный статус'
    mark_as_disabled.short_description = 'Неактивный статус'
    
    list_display = [
        'id',
        'header',
        'create_at',
        'updated_at',
        'publicised_at',
        'user',
        'activity'
    ]
    list_filter = ['activity']
    inlines = [CommentTabularInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Админка для списка комментариев
    """
    
    actions = ['removed_by_moder']
    
    def removed_by_moder(self, request, queryset):
        queryset.update(text='Удалено администратором')
    
    removed_by_moder.short_description = 'Неприемлемый контент'
    
    list_display = [
        'id',
        'news',
        'name',
        # 'user'
        'text',
        'create_at'
    ]
    list_filter = [
        'name'
    ]
