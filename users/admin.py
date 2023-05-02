from django.contrib import admin
from .models import Profile, Cars, Order, TypeOfRepair, PartsOrder, UndefinedParts
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    list_display_links = ('first_name', 'last_name', 'username')
    search_fields = ('last_name', 'first_name')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'type', 'date_field', 'status')
    list_display_links = ('id', 'user', 'last_name', 'first_name')
    search_fields = ('id', 'user__username', 'id', 'first_name', 'last_name')
    list_filter = ('status', 'user')


admin.site.register(Order, OrderAdmin)


class TypeOfRepairAdmin(admin.ModelAdmin):
    list_display = ('type',)
    list_display_links = ('type',)
    search_fields = ('type',)


admin.site.register(TypeOfRepair, TypeOfRepairAdmin)


class PartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'status')
    list_display_links = ('id', 'name', 'phone_number')
    search_fields = ('id', 'name',)
    list_filter = ('id', 'name', 'status')


admin.site.register(PartsOrder, PartsAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'image_show', 'first_name', 'last_name', 'is_new_user')
    list_display_links = ('user', 'image_show')
    search_fields = ('user__username', 'first_name', 'last_name')

    def car_image(self, obj):
        if obj.img_of_avto:
            return mark_safe("<img src='{}' width='60' />".format(obj.img_of_avto.url))
        return 'None'

    def image_show(self, obj):
        if obj.img:
            return mark_safe("<img src='{}' width='60' />".format(obj.img.url))
        return 'None'


admin.site.register(Profile, ProfileAdmin)


# Register your models here.
class CarsAdmin(admin.ModelAdmin):
    list_display = ('user', 'marka', 'model', 'car_image', 'is_main_car')
    list_display_links = ('user', 'car_image')
    search_fields = ('user', 'marka', 'model')

    def car_image(self, obj):
        if obj.img_of_avto:
            return mark_safe("<img src='{}' width='60' />".format(obj.img_of_avto.url))
        return 'None'


admin.site.register(Cars, CarsAdmin)


class UndefinedPartsAdmin(admin.ModelAdmin):
    list_display = ('id_order', 'name', 'product', 'count_product')
    list_display_links = ('id_order', 'name')
    search_fields = ('id_order', 'name', 'product')
    list_filter = ('name', 'product')


admin.site.register(UndefinedParts, UndefinedPartsAdmin)