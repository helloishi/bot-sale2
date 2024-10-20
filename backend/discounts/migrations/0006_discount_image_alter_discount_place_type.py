# Generated by Django 4.2.13 on 2024-07-16 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0005_delete_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='image',
            field=models.ImageField(blank=True, upload_to='images', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='place_type',
            field=models.CharField(blank=True, choices=[('REST', 'Ресторан'), ('CAFE', 'Кафе'), ('THTR', 'Театр'), ('SHOP', 'Магазин'), ('OTHR', 'Другое')], max_length=4, verbose_name='Тип заведения'),
        ),
    ]
