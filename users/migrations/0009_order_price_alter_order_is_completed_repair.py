# Generated by Django 4.0.1 on 2022-05-25 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_order_is_active_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_completed_repair',
            field=models.BooleanField(default=False, verbose_name='Авто забрали, розрахувались?'),
        ),
    ]
