from django.urls import path

from app_author.views import AuthorDetail
from app_author.views import AuthorList

urlpatterns = [
    path(
        'authors/',
        AuthorList.as_view(),
        name='author_list'
    ),
    path(
        'authors/<int:pk>/',
        AuthorDetail.as_view(),
        name='author_detail'
    )
]
