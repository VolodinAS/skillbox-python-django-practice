from django.db import models


class PriceCurrency(models.Model):
    """
    Валюты цен + бесплатный тип
    """
    code = models.CharField(
        max_length=10,
        verbose_name='Код валюты'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название валюты'
    )
    sign = models.CharField(
        max_length=5,
        verbose_name='Знак'
    )
    enabled = models.BooleanField(
        default=False,
        verbose_name='Доступен для выбора'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Сортировка отображения'
    )
    
    def __str__(self):
        return f'({self.sign}) {self.title} - {self.code}'
    
    class Meta:
        db_table = 'currencies'
        ordering = ['order']
