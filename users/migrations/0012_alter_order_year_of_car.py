# Generated by Django 4.0.1 on 2022-05-25 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_order_year_of_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='year_of_car',
            field=models.CharField(default='---------', max_length=10, verbose_name='Рік випуску авто'),
        ),
    ]
