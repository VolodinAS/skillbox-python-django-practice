from django.db import models
from django.urls import reverse


class House(models.Model):
    house_type = models.ForeignKey(
        'HouseType',
        on_delete=models.CASCADE,
        verbose_name='Тип помещения',
        related_name='house_type'
    )
    house_rooms = models.ForeignKey(
        'RoomsAmount',
        on_delete=models.CASCADE,
        verbose_name='Количество комнат',
        related_name='rooms_amount'
    )
    address = models.CharField(
        max_length=500,
        verbose_name='Адрес',
        blank=True
    )
    price = models.IntegerField(
        default=0,
        verbose_name='Цена (в тыс. у.е.)'
    )
    house_image = models.ImageField(
        upload_to='images/houses/',
        null=True,
        blank=True
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Последнее обновление'
    )
    
    def get_absolute_url(self):
        return reverse('houses:page_houses_detail', args=[str(self.id)])
    
    def __str__(self):
        return f'[{self.id}] - {self.house_type} - {self.house_rooms}'
    
    class Meta:
        ordering = ['id']
        verbose_name = 'жилое помещение'
        verbose_name_plural = 'жилые помещения'
        db_table = 'houses'


class HouseType(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    description = models.CharField(
        max_length=500,
        verbose_name='Описание'
    )
    prestige_grade = models.IntegerField(
        default=1,
        verbose_name='Уровень престижности'
    )
    
    def __str__(self):
        return f'(Престиж: {self.prestige_grade}) {self.title}'
    
    class Meta:
        ordering = ['prestige_grade']
        verbose_name = 'тип помещения'
        verbose_name_plural = 'типы помещений'
        db_table = 'house_types'


class RoomsAmount(models.Model):
    amount = models.IntegerField(
        default=1,
        verbose_name='Количество комнат'
    )
    
    def __str__(self):
        return f'{self.amount}-комнатная'
    
    class Meta:
        ordering = ['id']
        verbose_name = 'комната'
        verbose_name_plural = 'комнаты'
        db_table = 'house_rooms'
