# Generated by Django 4.1.4 on 2022-12-22 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_houses', '0008_house_house_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Последнее обновление'),
        ),
    ]
