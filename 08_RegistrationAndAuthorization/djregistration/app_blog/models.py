from django.contrib.auth.models import User
from django.db import models


class Blog(models.Model):
    """
    Список блогов
    """
    user = models.ForeignKey(
        User,
        related_name='blog',
        verbose_name='Создатель блога DJDB',
        on_delete=models.CASCADE
    )
    header = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    content = models.TextField(
        verbose_name='Текст',
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
    
    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        db_table = 'blogs'
        ordering = ['-create_at']


class BlogImages(models.Model):
    """
    Изображения для блога
    """
    blog = models.ForeignKey(
        Blog,
        related_name='blog_photos',
        on_delete=models.CASCADE,
        verbose_name='Блог'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='images/blogs/',
        null=True,
        blank=True
    )
    upload_at = models.DateTimeField(
        verbose_name='Дата загрузки',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'фотка блога'
        verbose_name_plural = 'фотки блога'
        db_table = 'blog_images'
        ordering = ['blog', '-upload_at']
