# Generated by Django 4.0.1 on 2022-05-25 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_order_price_alter_order_is_completed_repair'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='year_of_car',
            field=models.IntegerField(default=2022, verbose_name='Рік випуску авто'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(blank=True, default=0, verbose_name='Вартість послуги'),
        ),
    ]