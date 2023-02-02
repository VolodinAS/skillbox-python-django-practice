from django.conf import settings
from django.conf.urls.static import static
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
    path(
        'profile/',
        UserProfile.as_view(),
        name='user_profile'
    ),
    path(
        'profile/<int:pk>',
        ViewProfile.as_view(),
        name='view_profile'
    ),
    path(
        'verifyme/',
        UserVerify.as_view(),
        name='user_verify'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
