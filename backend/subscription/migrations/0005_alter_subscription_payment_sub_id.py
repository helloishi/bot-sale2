# Generated by Django 4.2.13 on 2024-07-23 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_subscription_payment_sub_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='payment_sub_id',
            field=models.CharField(default='', max_length=50, verbose_name='Идентификатор подписки CloudPayments'),
        ),
    ]
