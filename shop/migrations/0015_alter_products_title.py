# Generated by Django 4.0.1 on 2022-04-01 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_products_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
