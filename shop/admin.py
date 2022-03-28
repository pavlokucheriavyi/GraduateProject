from django.contrib import admin
from .models import Category, Products


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'count', 'category')
    list_display_links = ('title',)
    search_fields = ('title',)


admin.site.register(Products, ProductsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', )
    list_display_links = ('category',)
    search_fields = ('category',)


admin.site.register(Category, CategoryAdmin)





# Register your models here.
