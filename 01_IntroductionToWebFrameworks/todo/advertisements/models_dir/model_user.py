from django.db import models


class User(models.Model):
    """
    Пользователь
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Имя пользователя'
    )
    email = models.CharField(
        max_length=500,
        verbose_name='Email'
    )
    phone = models.CharField(
        max_length=200,
        verbose_name='Телефон'
    )
    
    def __str__(self):
        return f'{self.name} ({self.email})'
    
    class Meta:
        db_table = 'users'
        ordering = ['name']
