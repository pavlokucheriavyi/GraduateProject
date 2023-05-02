from django.db import models
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Products(models.Model):
    title = models.CharField("Назва", max_length=200, unique=True)
    price = models.DecimalField("Ціна", max_digits=10, decimal_places=2, default=0)
    description = models.TextField("Опис товару", blank=True)
    count = models.IntegerField("Кількість товару в наявності", default=0)
    date = models.DateTimeField("Дата", default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField("Фото товару", upload_to='details_photo', default='static/shop/fon.jpg')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class AvailableMarks(models.Model):
    name = models.CharField(max_length=200, blank=True)
    is_available = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Available Mark'
        verbose_name_plural = 'Available Marks'
        ordering = ['name']


class PidMarks(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Марка для підшипників'
        verbose_name_plural = 'Марки для підшипників'
        ordering = ['name']

