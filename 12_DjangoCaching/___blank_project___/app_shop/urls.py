from django.urls import path

from .views import *

urlpatterns = [
    path(
        '',
        ShopIndexListView.as_view(),
        name='shop_list'
    ),
]
