from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Blog(models.Model):
    """
    Список блогов
    """
    user = models.ForeignKey(
        User,
        related_name='blog',
        verbose_name=_('tid_models_blog_user'),  # 'Создатель блога DJDB'
        on_delete=models.CASCADE
    )
    header = models.CharField(
        max_length=200,
        verbose_name=_('tid_label_header'),  # 'Заголовок'
    )
    content = models.TextField(
        verbose_name=_('tid_models_blog_text'),  # 'Текст',
        max_length=5000
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('tid_blog_label_created_at'),  # 'Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('tid_blog_label_updated_at'),  # 'Дата обновления'
    )
    
    def __str__(self):
        return f'{self.header}'
    
    class Meta:
        verbose_name = _('tid_models_blog_meta_vn')  # 'блог'
        verbose_name_plural = _('tid_models_blog_meta_vnp')  # 'блоги'
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
        verbose_name=_('tid_models_blog_meta_vn'),  # 'Блог'
    )
    image = models.ImageField(
        verbose_name=_('tid_label_images'),  # 'Изображение',
        upload_to='images/blogs/',
        null=True,
        blank=True
    )
    upload_at = models.DateTimeField(
        verbose_name=_('tid_models_blog_images_upload_at'),  # 'Дата загрузки',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('tid_models_blog_images_meta_vn')  # 'фотка блога'
        verbose_name_plural = _('tid_models_blog_images_meta_vnp')  # 'фотки блога'
        db_table = 'blog_images'
        ordering = ['blog', '-upload_at']
