from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app_rss.feeds import LatestNewsFeed
from .views import *

app_name = 'rss'

urlpatterns = [
    path(
        'rss/',
        LatestNewsFeed(),
        name=''
    ),
]