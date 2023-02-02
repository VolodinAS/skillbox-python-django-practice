from django.urls import path

from app_basket.views import *

urlpatterns = [
    path('basket/', BasketView.as_view(), name='page_basket'),
    path('confirm/', confirm_order, name='page_basket_confirm'),
    path('order_paid/', BasketPaidListView.as_view(), name='page_paid_list'),
    path('order_paid/<int:pk>', BasketPaidDetailView.as_view(), name='page_paid'),

]
