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
import debug_toolbar
from django.contrib import admin
from django.urls import include

from django.urls import path


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n', include('django.conf.urls.i18n')),
    path('', include('app_market.urls')),
    path('', include('app_users.urls')),
    path('', include('app_basket.urls')),
    path('', include('app_reports.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('sentry-debug/', trigger_error),
]
