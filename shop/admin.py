from django.contrib import admin
from .models import Category, Products, AvailableMarks
from django.utils.safestring import mark_safe


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_show', 'price', 'count', 'category')
    list_display_links = ('title',)
    search_fields = ('title',)

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60' />".format(obj.image.url))
        return 'None'


admin.site.register(Products, ProductsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    list_display_links = ('category',)
    search_fields = ('category',)


admin.site.register(Category, CategoryAdmin)


class AvailableMarksAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_available')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(AvailableMarks, AvailableMarksAdmin)
# Register your models here.
