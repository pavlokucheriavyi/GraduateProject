# Generated by Django 4.0.1 on 2022-04-01 11:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_products_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
    ]