from django.contrib.auth.models import User
from django.db import models


class NewsItem(models.Model):
    """
    Одна новость
    """
    
    header = models.CharField(
        verbose_name='Заголовок',
        max_length=200
    )
    content = models.TextField(
        verbose_name='Содержание',
        max_length=5000
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
        auto_now_add=False,
        verbose_name='Дата публикации',
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        verbose_name='Чья новость (AbstractUser)',
        default=None,
        null=True,
        related_name='news_user',
        on_delete=models.CASCADE
    )
    published = models.BooleanField(
        default=False,
        verbose_name='Пройдена модерация'
    )
    published_by = models.ForeignKey(
        User,
        verbose_name='Кем опубликована (AbstractUser)',
        default=None,
        null=True,
        related_name='news_moder_user',
        on_delete=models.CASCADE
    )
    tag = models.CharField(
        verbose_name='Тег для новости',
        max_length=300
    )
    
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        db_table = 'news'
        ordering = ['-create_at']
        permissions = (
            ("can_publish", "Может публиковать"),
        )
