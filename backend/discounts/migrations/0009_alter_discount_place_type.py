# Generated by Django 4.2.13 on 2024-07-24 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0008_alter_discount_address_txt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='place_type',
            field=models.CharField(blank=True, choices=[('CAFE', 'Кафе'), ('REST', 'Рестораны'), ('SHOP', 'Магазины'), ('DSUG', 'Досуг'), ('BTY', 'Красота'), ('SPRT', 'Спорт'), ('OTHR', 'Другое')], max_length=4, verbose_name='Тип заведения'),
        ),
    ]
