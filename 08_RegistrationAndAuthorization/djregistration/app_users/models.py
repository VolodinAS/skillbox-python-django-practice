import os

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Чей профиль (AbstractUser)'
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Город проживания'
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения'
    )
    phone = models.CharField(
        max_length=30,
        verbose_name='Телефон'
    )
    avatar_file = models.ImageField(
        upload_to='images/user_avatars/',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
        db_table = 'profile'
        ordering = ['id']
