from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsItem(models.Model):
    """
    Одна новость
    """
    
    header = models.CharField(
        verbose_name=_('tid_label_header'),  # 'Заголовок',
        max_length=200
    )
    content = models.TextField(
        verbose_name=_('tid_label_content'),  # 'Содержание',
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
    publicised_at = models.DateTimeField(
        auto_now_add=False,
        verbose_name=_('tid_news_label_published_at'),  # 'Дата публикации',
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('tid_models_blog_user'),  # 'Чья новость (AbstractUser)',
        default=None,
        null=True,
        related_name='news_user',
        on_delete=models.CASCADE
    )
    published = models.BooleanField(
        default=False,
        verbose_name=_('tid_news_label_published_at'),  # 'Пройдена модерация'
    )
    published_by = models.ForeignKey(
        User,
        verbose_name=_('tid_models_news_item_published_by'),  # 'Кем опубликована (AbstractUser)',
        default=None,
        null=True,
        related_name='news_moder_user',
        on_delete=models.CASCADE
    )
    tag = models.CharField(
        verbose_name=_('tid_label_tag'),  # 'Тег для новости',
        max_length=300
    )
    
    def __str__(self):
        return f'"{self.header}" - {self.user.username}'
    
    class Meta:
        verbose_name = _('tid_models_news_meta_vn')  # 'новость'
        verbose_name_plural = _('tid_models_news_meta_vnp')  # 'новости'
        db_table = 'news'
        ordering = ['-create_at']
        permissions = (
            ("can_publish", _('tid_models_news_meta_perm_can_publish')),
        )
