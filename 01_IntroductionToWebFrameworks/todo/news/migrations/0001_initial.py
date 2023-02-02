# Generated by Django 4.1.3 on 2022-12-04 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('advertisements', '0005_alter_advertisement_publicised_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(default='', max_length=200, verbose_name='Заголовок')),
                ('content', models.TextField(default='', max_length=5000, verbose_name='Содержание')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('publicised_at', models.DateTimeField(verbose_name='Дата публикации')),
                ('activity', models.BooleanField(default=False, verbose_name='Флаг активности')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news_userer', to='advertisements.user', verbose_name='Пользователь')),
            ],
            options={
                'db_table': 'news',
                'ordering': ['header'],
            },
        ),
    ]