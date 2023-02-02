from django.db import models

from app_author.models import Author


class Book(models.Model):
    """
    Модель книги
    """
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='rel_author',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=1000,
        verbose_name='Название'
    )
    isbn = models.CharField(
        max_length=200,
        verbose_name='ISBN'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    pages = models.IntegerField(
        verbose_name='Количество страниц'
    )

    def __str__(self):
        return f'«{self.title}», {self.author.last_name} {self.author.first_name}, {self.year}'

    class Meta:
        """
        Мета-класс Книги
        """
        verbose_name = 'книга'
        verbose_name_plural = 'книги'
        db_table = 'books'
        ordering = ['title', 'year', 'pages']
