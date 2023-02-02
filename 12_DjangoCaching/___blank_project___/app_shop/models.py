from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Shop(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name=_('Название магазина')
    )
    promotions = models.ManyToManyField(
        'Promotion',
        related_name='promotions',
        verbose_name=_('Акции'),  #
    )
    offers = models.ManyToManyField(
        'Offer',
        related_name='offers',
        verbose_name=_('Предложения'),  #
    )
    
    def get_promotions(self):
        return self.promotions.all()
    
    def get_offers(self):
        return self.offers.all()
    
    def __str__(self):
        return f'«{self.title}»'
    
    class Meta:
        ordering = ['title']
        verbose_name = _('магазин')
        verbose_name_plural = _('магазины')
        db_table = 'shops'


class Promotion(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_('Заголовок'),  #
    )
    description = models.TextField(
        max_length=1000,
        verbose_name=_('Описание'),  #
    )
    expire_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Срок окончания'),  #
    )
    is_archive = models.BooleanField(
        default=False,
        verbose_name=_('Архив'),  #
    )
    
    def __str__(self):
        return f'«{self.title}» - {self.expire_at.strftime("%Y-%m-%d %H:%M:%S")}'
    
    class Meta:
        ordering = ['-expire_at']
        verbose_name = _('акция')
        verbose_name_plural = _('акции')
        db_table = 'promotions'


class Offer(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_('Заголовок'),  #
    )
    description = models.TextField(
        max_length=1000,
        verbose_name=_('Описание'),  #
    )
    expire_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Срок окончания'),  #
    )
    is_archive = models.BooleanField(
        default=False,
        verbose_name=_('Архив'),  #
    )
    
    def __str__(self):
        return f'«{self.title}» - {self.expire_at.strftime("%Y-%m-%d %H:%M:%S")}'
    
    class Meta:
        ordering = ['-expire_at']
        verbose_name = _('предложение')
        verbose_name_plural = _('предложения')
        db_table = 'offers'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
        related_name='user'
    )
    goods_amount = models.IntegerField(
        default=0,
        verbose_name=_('Количество товара')
    )
    total_money = models.FloatField(
        default=0,
        verbose_name=_('Сумма покупки')
    )
    paid_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата покупки')  #
    )

    def __str__(self):
        return f'{self.user.username} - {self.goods_amount} - {self.total_money} - {self.paid_at.strftime("%Y-%m-%d %H:%M:%S")}'

    class Meta:
        ordering = ['-paid_at']
        verbose_name = _('покупка')
        verbose_name_plural = _('покупки')
        db_table = 'orders'

