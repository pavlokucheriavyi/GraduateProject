from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Products(models.Model):
    title = models.CharField(max_length=200, unique=True)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='details_photo', default='static/fon.jpg')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

