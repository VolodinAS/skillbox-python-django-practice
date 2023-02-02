from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from django_example.views import MainView

urlpatterns = [
    # path('', MainView.as_view(), name='main'),
    path('app_logic/', include('app_logic.urls')),
    path('app_goods/', include('app_goods.urls')),
    path('app_users/', include('app_users.urls')),
    path('', include('app_pages.urls')),
    path('i18n', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
