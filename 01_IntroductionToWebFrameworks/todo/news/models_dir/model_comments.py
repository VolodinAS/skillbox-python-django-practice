from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    """
    Комментарии
    """
    news = models.ForeignKey(
        'NewsItem',
        default=None,
        null=True,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Новость'
    )
    name = models.CharField(
        verbose_name='Имя комментатора',
        max_length=200
    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=1000
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь из DJBD',
        default=None,
        null=True,
        related_name='users',
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f'{self.text}'
    
    class Meta:
        db_table = 'commentaries'
        ordering = ['-create_at']
