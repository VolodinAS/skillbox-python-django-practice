# Generated by Django 4.1.4 on 2022-12-23 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0010_alter_profile_avatar_file_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='balance',
            field=models.FloatField(default=0, verbose_name='Баланс'),
        ),
    ]
