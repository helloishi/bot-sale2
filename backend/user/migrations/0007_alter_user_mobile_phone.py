# Generated by Django 4.2.13 on 2024-07-13 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_name_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=50, verbose_name='Номер телефона (с 8)'),
        ),
    ]
