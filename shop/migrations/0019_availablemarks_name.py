# Generated by Django 4.0.1 on 2022-04-27 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_availablemarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='availablemarks',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
