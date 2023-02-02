from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Модель профиля
    """
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
    balance = models.FloatField(
        verbose_name='Баланс',
        default=0
    )
    user_status = models.IntegerField(
        verbose_name='ID старого статуса',
        default=1
    )
    
    def __str__(self):
        return f'{self.user.username} - {self.balance}'
    
    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
        db_table = 'profile'
        ordering = ['id']


class UserStatus(models.Model):
    """
    Модель статуса
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Титул'
    )
    expenses_lt = models.IntegerField(
        verbose_name='Порог перехода'
    )
    
    def __str__(self):
        return f'{self.title} - {self.expenses_lt}'
    
    class Meta:
        verbose_name = 'статус'
        verbose_name_plural = 'статусы'
        db_table = 'statuses'
        ordering = ['expenses_lt']
