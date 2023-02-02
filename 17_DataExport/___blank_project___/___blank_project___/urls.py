"""___blank_project___ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include
from django.urls import path

from app_about.sitemap import AboutSiteMap
from app_contacts.sitemap import ContactsSiteMap
from app_houses.sitemap import HousesSiteMap
from app_news.sitemap import NewsSiteMap

sitemaps = {
    'news': NewsSiteMap,
    'houses': HousesSiteMap,
    'about': AboutSiteMap,
    'contacts': ContactsSiteMap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n', include('django.conf.urls.i18n')),
    path('', include('app_houses.urls', namespace='houses')),
    path('', include('app_about.urls', namespace='about')),
    path('', include('app_contacts.urls', namespace='contacts')),
    path('', include('app_news.urls', namespace='news')),
    path('', include('app_rss.urls', namespace='rss')),
    path('sitemap.xml', sitemap, {
        'sitemaps': sitemaps
    }, name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
