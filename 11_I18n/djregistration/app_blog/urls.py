from django.urls import path

from .views import *

urlpatterns = [
    path(
        'blogs/',
        BlogsListView.as_view(),
        name='page_blog_index'
    ),
    path(
        'blogs/add/',
        BlogAddView.as_view(),
        name='page_blog_add'
    ),
    path(
        'blogs/import/',
        BlogImportView.as_view(),
        name='page_blog_import'
    ),
    path(
        'blogs/<int:pk>',
        BlogDetailView.as_view(),
        name='page_blog_detail'
    ),
    path(
        'myblog/',
        BlogMyListView.as_view(),
        name='page_my_blog'
    ),
]
