from django.urls import path

from .views import *

urlpatterns = [
    path(
        '',
        Index.as_view(),
        name='news_index'
    ),
    path(
        '<int:pk>',
        NewsDetails.as_view(),
        name='news_details'
    ),
    path(
        '<int:pk>/edit',
        EditNewsItem.as_view(),
        name='news_edit'
    ),
    path(
        'add',
        AddNews.as_view(),
        name='news_add'
    )
    # path(
    #     'contacts',
    #     Contacts.as_view(),
    #     name='page_contacts'
    # ),
    # path(
    #     'about',
    #     About.as_view(),
    #     name='page_about'
    # ),
    # path(
    #     'advertisements/',
    #     AdvertisementList.as_view(),
    #     name='page_advertisements'
    # ),
    # path(
    #     'advertisements/<int:pk>',
    #     AdvertisementDetails.as_view(),
    #     name='page_advertisement_details'
    # ),
]
