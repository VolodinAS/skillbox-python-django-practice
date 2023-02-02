from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

app_name = 'contacts'

urlpatterns = [
    path(
        'contacts',
        ContactsView.as_view(),
        name='page_houses_contacts'
    ),
]
