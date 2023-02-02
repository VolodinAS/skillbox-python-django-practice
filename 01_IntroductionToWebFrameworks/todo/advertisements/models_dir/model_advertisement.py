from django.db import models


# Create your models here.
class Advertisement(models.Model):
    """
    Объявление
    """
    title = models.CharField(
        max_length=1500,
        verbose_name='Заголовок'
    )
    description = models.CharField(
        max_length=1000,
        default='',
        verbose_name='Описание'
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    publicised_at = models.DateTimeField(
        auto_now=False,
        verbose_name='Дата публикации'
    )
    user = models.ForeignKey(
        'User',
        default=None,
        null=True,
        related_name='userer',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    category = models.ForeignKey(
        'Category',
        default=None,
        null=True,
        related_name='categorier',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    price_value = models.FloatField(
        verbose_name='Цена в у.е.',
        default=0,
    )
    price_currency = models.ForeignKey(
        'PriceCurrency',
        default=None,
        null=True,
        on_delete=models.CASCADE,
        related_name='currencier',
        verbose_name='Валюта'
    )
    views_count = models.IntegerField(
        verbose_name='Количество просмотров',
        default=0
    )
    status = models.ForeignKey(
        'AdvertisementStatus',
        default=None,
        null=True,
        on_delete=models.CASCADE,
        related_name='statuser',
        verbose_name='Статус'
    )
    region = models.ForeignKey(
        'Region',
        default=None,
        null=True,
        on_delete=models.CASCADE,
        related_name='regioner',
        verbose_name='Регион'
    )
    typer = models.ForeignKey(
        'AdvertisementType',
        default=None,
        null=True,
        on_delete=models.CASCADE,
        related_name='typer',
        verbose_name='Тип'
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'advertisements'
        ordering = ['title']


class Category(models.Model):
    """
    Категория объявления
    """
    title = models.CharField(
        max_length=100,
        verbose_name='Название категории'
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'categories'
        ordering = ['title']


class AdvertisementStatus(models.Model):
    """
    Статусы объявлений
    """
    title = models.CharField(
        max_length=100,
        verbose_name='Название статуса'
    )
    enabled = models.BooleanField(
        default=False,
        verbose_name='Доступен для выбора'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Сортировка отображения'
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'advertisement_statuses'
        ordering = ['order']


class Region(models.Model):
    """
    Регион объявления
    """
    title = models.CharField(
        max_length=100,
        verbose_name='Название региона'
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'regions'
        ordering = ['title']


class AdvertisementType(models.Model):
    """
    Тип объявления
    """
    title = models.CharField(
        max_length=100,
        verbose_name='Тип объявления'
    )
    enabled = models.BooleanField(
        default=False,
        verbose_name='Доступен для выбора'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Сортировка отображения'
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'advertisement_types'
        ordering = ['order']
