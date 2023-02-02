from django.contrib import admin

from .models import *


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'house_type',
        'house_rooms',
        'address',
        'price',
        'last_update',
        'house_image'
    ]


@admin.register(HouseType)
class HouseTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'description'
    ]


@admin.register(RoomsAmount)
class RoomsAmountAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'amount'
    ]
