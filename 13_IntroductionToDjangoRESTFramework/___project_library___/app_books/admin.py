from django.contrib import admin

from app_books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'title',
        'isbn',
        'year',
        'pages'
    ]
