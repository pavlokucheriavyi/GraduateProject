# Generated by Django 4.0.1 on 2022-03-14 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_category_options_alter_products_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(default='static/fon.png', height_field=50, upload_to='details_photo', width_field=50),
        ),
    ]
