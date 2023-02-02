from django.db import models


class NewsItem(models.Model):
    """
    Одна новость
    """
    
    
    
    header = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        default=''
    )
    content = models.TextField(
        verbose_name='Содержание',
        max_length=5000,
        default=''
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
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    user = models.ForeignKey(
        'advertisements.User',
        default=None,
        null=True,
        related_name='news_userer',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    activity = models.BooleanField(
        default=False,
        verbose_name='Флаг активности'
    )
    
    def __str__(self):
        return f'[{self.id}] {self.header} ({self.create_at.strftime("%Y-%m-%d %H:%M:%S")})'
    
    class Meta:
        db_table = 'news'
        ordering = ['-publicised_at']
