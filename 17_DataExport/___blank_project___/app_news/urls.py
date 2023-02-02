from django.urls import path

from .views import *

app_name = 'news'

urlpatterns = [
    path(
        'news',
        NewsListView.as_view(),
        name='page_houses_news'
    ),
    path(
        'news/<int:pk>',
        NewsItemDetailView.as_view(),
        name='page_houses_news_item'
    ),
]
