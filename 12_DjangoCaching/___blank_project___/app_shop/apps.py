from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_shop'
    verbose_name = _('Приложение «Магазины»')
