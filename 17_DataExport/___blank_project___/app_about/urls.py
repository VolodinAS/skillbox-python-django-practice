from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

app_name = 'about'

urlpatterns = [
    path(
        'about',
        AboutView.as_view(),
        name='page_houses_about'
    ),
]