# Generated by Django 4.2.13 on 2024-07-03 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0002_alter_discount_end_date_alter_discount_start_date'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fav_places',
            field=models.ManyToManyField(to='discounts.place', verbose_name='Избранные места'),
        ),
    ]
