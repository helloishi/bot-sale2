# Generated by Django 4.2.13 on 2024-07-03 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Когда создано')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Когда обновлено')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=60, verbose_name='Название')),
                ('address', models.TextField(verbose_name='Адрес')),
                ('description', models.TextField(verbose_name='Описание')),
                ('place_type', models.CharField(choices=[('RE', 'Ресторан'), ('CA', 'Кафе'), ('CF', 'Кофейня')], max_length=2, verbose_name='Тип заведения')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Когда создано')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Когда обновлено')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Описание')),
                ('start_date', models.DateField(verbose_name='')),
                ('end_date', models.DateField(verbose_name='')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.place', verbose_name='Заведение')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
