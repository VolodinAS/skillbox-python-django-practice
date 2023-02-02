from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        verbose_name=_('tid_headermenu_news'),  # 'Новость'
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('tid_models_blog_user'),  # 'Кто написал (AbstractUser)',
        default=None,
        null=True,
        related_name='comment_user',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name=_('tid_models_blog_text'),  # 'Текст',
        max_length=1000
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('tid_blog_label_created_at'),  # 'Дата создания'
    )
    
    class Meta:
        verbose_name = _('tid_models_comments_meta_vn')  # 'комментарий'
        verbose_name_plural = _('tid_models_comments_meta_vnp')  # 'комментарии'
        db_table = 'commentaries'
        ordering = ['-create_at']
