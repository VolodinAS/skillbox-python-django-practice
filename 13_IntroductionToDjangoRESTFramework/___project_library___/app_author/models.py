from django.db import models


# Create your models here.
class Author(models.Model):
    """
    Модель Автора
    """
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия'
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения'
    )
    
    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.birthday})'

    class Meta:
        """
        Мета-класс Автора
        """
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'
        db_table = 'authors'
        ordering = ['last_name', 'first_name', 'birthday']
        unique_together = ['first_name', 'last_name', 'birthday']
