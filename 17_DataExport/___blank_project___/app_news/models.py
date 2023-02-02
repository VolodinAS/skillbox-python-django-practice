from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.urls import reverse


class News(models.Model):
    title = models.CharField(
        max_length=500,
        verbose_name='Заголовок'
    )
    content = models.TextField(
        max_length=5000,
        verbose_name='Содержимое'
    )
    published_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата публикации',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Создатель',
        on_delete=models.CASCADE,
        related_name='author'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовать новость'
    )
    
    def get_absolute_url(self):
        return reverse('news:page_houses_news_item', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.title}, {self.author.username} ({self.published_at.strftime("%Y-%m-%d %H:%M:%S")})'
    
    class Meta:
        ordering = ['-is_published', '-published_at']  # сначала опубликованные, которые потом сортируются по свежести
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        db_table = 'news'
