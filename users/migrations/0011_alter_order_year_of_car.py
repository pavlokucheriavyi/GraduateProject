# Generated by Django 4.0.1 on 2022-05-25 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_order_year_of_car_alter_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='year_of_car',
            field=models.IntegerField(default=0, verbose_name='Рік випуску авто'),
        ),
    ]
