from django.contrib import admin

from .models_dir import *


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvertisementStatus)
class AdvertisementStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvertisementType)
class AdvertisementTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(PriceCurrency)
class PriceCurrencyAdmin(admin.ModelAdmin):
    pass
