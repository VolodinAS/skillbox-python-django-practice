# Generated by Django 4.1.4 on 2022-12-16 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_market', '0004_alter_good_shop_alter_goodimages_good_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='amount',
            field=models.FloatField(default=1, verbose_name='Количество'),
        ),
    ]
