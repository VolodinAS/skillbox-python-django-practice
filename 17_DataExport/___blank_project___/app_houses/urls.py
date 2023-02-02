from django.urls import path

from .views import *

app_name = 'houses'

urlpatterns = [
    path(
        '',
        HouseListView.as_view(),
        name='page_houses_index'
    ),
    path(
        '<int:pk>',
        HouseDetailView.as_view(),
        name='page_houses_detail'
    ),
]
