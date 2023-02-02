from django.urls import path

from .views import GroupsListView
from .views import OrderCreateView
from .views import OrderDeleteView
from .views import OrderUpdateView
from .views import OrdersDetailView
from .views import OrdersListView
from .views import ProductCreateView
from .views import ProductDeleteView
from .views import ProductDetailView
from .views import ProductListView
from .views import ProductUpdateView
from .views import ShopIndexView

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/create", ProductCreateView.as_view(), name="products_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="products_details"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="products_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="products_delete"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/create", OrderCreateView.as_view(), name="orders_create"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="orders_details"),
    path("orders/<int:pk>/edit", OrderUpdateView.as_view(), name="orders_update"),
    path("orders/<int:pk>/delete", OrderDeleteView.as_view(), name="orders_delete"),
]
