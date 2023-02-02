from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppBlogConfig(AppConfig):
    """
    Конфиг Блога
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_blog'
    verbose_name = _('tid_admin_blog')
