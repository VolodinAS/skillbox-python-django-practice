from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_news'
    verbose_name = _('tid_admin_news')
