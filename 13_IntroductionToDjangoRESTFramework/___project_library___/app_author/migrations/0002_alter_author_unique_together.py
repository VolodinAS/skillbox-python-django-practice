# Generated by Django 4.1.4 on 2022-12-14 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_author', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='author',
            unique_together={('first_name', 'last_name', 'birthday')},
        ),
    ]