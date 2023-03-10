# Generated by Django 4.1.4 on 2022-12-16 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.CharField(max_length=500, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/goods/')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('remains', models.IntegerField(default=0, verbose_name='Остаток')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'db_table': 'goods',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата формирования заказа')),
                ('paid_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата оплаты заказ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'наряд-заказ',
                'verbose_name_plural': 'наряд-заказы',
                'db_table': 'orders',
                'ordering': ['create_at'],
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'магазин',
                'verbose_name_plural': 'магазины',
                'db_table': 'shops',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, verbose_name='Цена на момент заказа')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good', to='app_market.good', verbose_name='Товар')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='app_market.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'товар в заказе',
                'verbose_name_plural': 'товары заказа',
                'db_table': 'order_items',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='good',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to='app_market.shop', verbose_name='Магазин'),
        ),
    ]
