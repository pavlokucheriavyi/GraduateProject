from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from shop.models import Products
from django.contrib.auth import get_user_model


class PartsOrder(models.Model):
    name = models.CharField('Ім`я, прізвище', max_length=200)
    email = models.CharField('Email користувача', max_length=200, blank=True)
    phone_number = PhoneNumberField('Номер телефону')
    address_city = models.CharField('Адреса міста доставки', max_length=200, default='САМОВИВІЗ')
    address_vidd = models.CharField('Адреса відділення доставки', max_length=200, default="САМОВИВІЗ")
    comment = models.TextField('Коментар до замовлення', default='---------')
    composition_order = models.TextField('Замовлення')
    sizes = (
        ('Замовлення в процесі', 'Замовлення в процесі'),
        ('Користувач забрав товар', 'Користувач забрав товар'),
        ('Користувач не розрахувався', 'Користувач не розрахувався')
    )
    summa = models.CharField('Сума (грн)', max_length=15, default='')
    status = models.CharField('Статус', max_length=200, choices=sizes, default='Замовлення в процесі')
    is_authenticated_user = models.CharField('id користувача або не зареєстрований(0)', max_length=20, default="Не зареєстрований")
    date_field = models.DateTimeField('Дата замовлення', default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.status == 'Користувач забрав товар':
            un_parts = UndefinedParts.objects.filter(id_order=self.id)
            for i in un_parts:
                i.delete()
            if self.is_authenticated_user != '0':
                get_user = Profile.objects.get(user_id=int(self.is_authenticated_user))
                get_user.is_new_user = False
                get_user.save()

        elif self.status == 'Користувач не розрахувався':
            un_parts = UndefinedParts.objects.filter(id_order=self.id)
            for item in un_parts:
                try:
                    product_object = Products.objects.get(id=item.id_of_product)
                    product_object.count += item.count_product
                    product_object.save()
                    item.delete()
                except Products.DoesNotExist:
                    item.delete()
        return super(PartsOrder, self).save()

    class Meta:
        verbose_name = 'Замовлення запчастин'
        verbose_name_plural = 'Замовлення запчастин'


class UndefinedParts(models.Model):
    id_order = models.IntegerField("ID замовлення")
    name = models.CharField("Ім'я замовника", max_length=100)
    product = models.CharField("Назва продукту", max_length=50)
    id_of_product = models.IntegerField("ID продукту", default=1)
    count_product = models.IntegerField("Кількість замовленого продукту")
    date_field = models.DateTimeField('Дата замовлення', default=timezone.now)

    def __str__(self):
        x = str(self.id_order)
        return x

    class Meta:
        verbose_name = 'Не визначені запчастини'
        verbose_name_plural = 'Не визначені запчастини'


class TypeOfRepair(models.Model):
    type = models.CharField(max_length=200)
    icon = models.ImageField('Іконка', default='shop/static/shop/shinomontazh.png', upload_to='user_images')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип замовлення'
        verbose_name_plural = 'Типи замовлення'


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField('Ім`я клієнта', max_length=200, default="Ім'я не вказане")
    last_name = models.CharField('Прізвище клієнта', max_length=200, default="Прізвище не вказане")
    phone_number = PhoneNumberField('Номер телефону', blank=True)
    type = models.ForeignKey(TypeOfRepair, verbose_name='Тип ремонту', on_delete=models.CASCADE)
    marka = models.CharField('Авто (марка)', max_length=200, default="Авто не вказане", blank=True)
    model = models.CharField('Авто (модель)', max_length=200, default="Авто не вказане", blank=True)
    year_of_car = models.CharField('Рік випуску авто', max_length=10, default='---------')
    price = models.CharField('Вартість послуги', max_length=10, default='Наразі не встановлена')
    sizes = (
        ('Замовлення принято', 'Замовлення принято'),
        ('В процесі ремонту', 'В процесі ремонту'),
        ('Готово', 'Готово'),
        ('Ремонт закінчений', 'Ремонт закінчений')
    )
    status = models.CharField('Статус', max_length=200, choices=sizes, default='Замовлення принято')
    date_field = models.DateTimeField('Дата замовлення', default=timezone.now)
    is_completed_repair = models.BooleanField('Авто забрали, розрахувались?', default=False)

    def __str__(self):
        return f'Замовлення користувача {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Замовлення ремонту'
        verbose_name_plural = 'Замовлення ремонту'


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Користувач', on_delete=models.CASCADE)
    img = models.ImageField('Фото користувача', default='shop/static/shop/profile.png', upload_to='user_images')
    first_name = models.CharField('Ім`я', max_length=200, default="Ім'я не вказане")
    last_name = models.CharField('Прізвище', max_length=200, default="Прізвище не вказане")
    email = models.CharField('Email', max_length=100, default='abracadabra@ukr.net')
    is_new_user = models.BooleanField('Новий користувач?', default=True)

    def __str__(self):
        return f'Профіль користувача {self.user.username}'

    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.img.path)

        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'


class Cars(models.Model):
    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)
    marka = models.CharField(max_length=200, default="Авто не вказане")
    model = models.CharField(max_length=200, default="Авто не вказане")
    img_of_avto = models.ImageField('Фото авто', default='shop/static/shop/car.jpg', upload_to='users_cars')
    is_main_car = models.BooleanField('Головна машина?', default=False)
    date_field = models.DateTimeField('Дата', default=timezone.now)

    def __str__(self):
        return f'Авто користувача {self.user.username}'

    class Meta:
        verbose_name = 'Авто'
        verbose_name_plural = 'Автомобілі'
# Create your models here.
