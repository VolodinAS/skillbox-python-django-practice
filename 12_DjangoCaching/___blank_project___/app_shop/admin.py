from django.contrib import admin

# Register your models here.
from app_shop.models import Offer
from app_shop.models import Order
from app_shop.models import Promotion
from app_shop.models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'get_promotions',
        'get_offers'
    ]
    list_display_links = ['title']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Promotion._meta.get_fields()]


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Offer._meta.get_fields()]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.get_fields()]
