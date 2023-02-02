from django.urls import path
from .views import item_list, update_prices

urlpatterns = [
    path('items', item_list, name='item_list'),
    path('update_prices', update_prices, name='update_prices'),
]
