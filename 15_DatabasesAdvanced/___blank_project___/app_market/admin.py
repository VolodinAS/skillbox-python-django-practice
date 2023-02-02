from django.contrib import admin

from app_market.models import *


class GoodImagesTabularInline(admin.TabularInline):
    """
    Админка редактирования товара с дополненными фотками
    """
    model = GoodImages


class OrderItemTabularInline(admin.TabularInline):
    """
    Админка редактирования товаров наряд-заказа
    """
    model = OrderItem


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """
    Админка магазинов
    """
    list_display = [
        'id',
        'title',
    ]


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    """
    Админка товаров с привязкой фоток
    """
    list_display = [
        'id',
        'title',
        'description',
        'shop',
        'face_image',
        'price',
        'remains',
    ]
    inlines = [GoodImagesTabularInline]


@admin.register(GoodImages)
class GoodImagesAdmin(admin.ModelAdmin):
    """
    Админка изображений
    """
    list_display = [
        'id',
        'good',
        'image'
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Админка наряд-заказов
    """
    list_display = [
        'id',
        'user',
        'create_at',
        'paid_at',
    ]
    inlines = [OrderItemTabularInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Админка товаров в нарядах-заказах
    """
    list_display = [
        'id',
        'order',
        'good',
        'price',
        'amount',
    ]
