# Generated by Django 4.2.13 on 2024-07-10 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_user_fav_places_user_fav_discounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=11, verbose_name='Номер телефона (с 8)'),
        ),
    ]
