# Generated by Django 4.0.1 on 2022-06-13 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_undefinedparts_id_of_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_new_user',
            field=models.BooleanField(default=True, verbose_name='Новий користувач?'),
        ),
    ]
