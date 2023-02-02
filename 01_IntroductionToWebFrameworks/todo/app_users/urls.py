from django.urls import path

from .views import *

urlpatterns = [
    path(
        'login/',
        LoginAuthView.as_view(),
        name='auth_login'
    ),
    path(
        'logout/',
        LogoutAuthView.as_view(),
        name='auth_logout'
    ),
    path(
        'reg/',
        RegView.as_view(),
        name='auth_reg'
    ),
]
