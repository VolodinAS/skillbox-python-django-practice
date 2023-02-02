from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    """
    Комментарии к новостям
    """
    news = models.ForeignKey(
        'app_news.NewsItem',
        default=None,
        null=True,
        related_name='comment_news_item',
        on_delete=models.CASCADE,
        verbose_name='Новость'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Кто написал (AbstractUser)',
        default=None,
        null=True,
        related_name='comment_user',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=1000
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        db_table = 'commentaries'
        ordering = ['-create_at']
