from django.urls import path

from .views import AddNewsView
from .views import MyNewsDetailView
from .views import MyNewsView
from .views import NewsIndex
from .views import NewsItemView
from .views import NewsModerDetailView
from .views import NewsModerListView
from .views import NewsPublish
from .views import TagSearch

urlpatterns = [
    path(
        '',
        NewsIndex.as_view(),
        name='page_index'
    ),
    path(
        '<int:pk>',
        NewsItemView.as_view(),
        name='page_news_item'
    ),
    path(
        'news/add/',
        AddNewsView.as_view(),
        name='page_news_add'
    ),
    path(
        'mynews/',
        MyNewsView.as_view(),
        name='page_my_news'
    ),
    path(
        'mynews/<int:pk>',
        MyNewsDetailView.as_view(),
        name='page_my_news_detail'
    ),
    path(
        'newsmoder/',
        NewsModerListView.as_view(),
        name='page_news_moder'
    ),
    path(
        'newsmoder/<int:pk>',
        NewsModerDetailView.as_view(),
        name='page_my_news_detail_moder'
    ),
    path(
        'newsmoder/publish/',
        NewsPublish.as_view(),
        name='page_news_moder_publish'
    ),
    path(
        'tagsearch',
        TagSearch.as_view(),
        name='page_tag_search'
    )
]
