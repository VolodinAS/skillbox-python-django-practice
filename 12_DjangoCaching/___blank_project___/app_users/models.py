import os
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь')
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Город проживания')
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Дата рождения')
    )
    phone = models.CharField(
        blank=True,
        max_length=30,
        verbose_name=_('Телефон')
    )
    avatar_file = models.ImageField(
        verbose_name=_('Аватар'),
        upload_to='images/user_avatars/',
        null=True,
        blank=True
    )
    balance = models.FloatField(
        verbose_name=_('Баланс'),
        default=0
    )
    
    class Meta:
        verbose_name = _('профиль')
        verbose_name_plural = _('профили')
        db_table = 'profile'
        ordering = ['id']
