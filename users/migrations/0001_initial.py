# Generated by Django 4.0.1 on 2022-05-23 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeOfRepair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Тип замовлення',
                'verbose_name_plural': 'Типи замовлення',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(default='shop/static/shop/profile.png', upload_to='user_images', verbose_name='Фото користувача')),
                ('first_name', models.CharField(default="Ім'я не вказане", max_length=200, verbose_name='Ім`я')),
                ('last_name', models.CharField(default='Прізвище не вказане', max_length=200, verbose_name='Прізвище')),
                ('marka', models.CharField(default='Авто не вказане', max_length=200, verbose_name='Головне авто (марка)')),
                ('model', models.CharField(default='Авто не вказане', max_length=200, verbose_name='Головне авто (модель)')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Профіль',
                'verbose_name_plural': 'Профілі',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default="Ім'я не вказане", max_length=200, verbose_name='Ім`я клієнта')),
                ('last_name', models.CharField(default='Прізвище не вказане', max_length=200, verbose_name='Прізвище клієнта')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Номер телефону')),
                ('marka', models.CharField(blank=True, default='Авто не вказане', max_length=200, verbose_name='Авто (марка)')),
                ('model', models.CharField(blank=True, default='Авто не вказане', max_length=200, verbose_name='Авто (модель)')),
                ('status', models.CharField(choices=[('Замовлення принято', 'Замовлення принято'), ('В процесі ремонту', 'В процесі ремонту'), ('Готово', 'Готово'), ('Ремонт закінчений', 'Ремонт закінчений')], default='Замовлення принято', max_length=200, verbose_name='Статус')),
                ('date_field', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата замовлення')),
                ('is_active_order', models.BooleanField()),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.typeofrepair', verbose_name='Тип ремонту')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Замовлення',
                'verbose_name_plural': 'Замовлення',
            },
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marka', models.CharField(default='Авто не вказане', max_length=200)),
                ('model', models.CharField(default='Авто не вказане', max_length=200)),
                ('img_of_avto', models.ImageField(default='shop/static/shop/car.jpg', upload_to='users_cars', verbose_name='Фото авто')),
                ('date_field', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Авто',
                'verbose_name_plural': 'Автомобілі',
            },
        ),
    ]
