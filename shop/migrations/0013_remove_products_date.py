# Generated by Django 4.0.1 on 2022-04-01 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_alter_products_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='date',
        ),
    ]
