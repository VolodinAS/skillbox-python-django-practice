# Generated by Django 4.1.4 on 2022-12-22 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_houses', '0007_alter_house_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='house_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/houses/'),
        ),
    ]
