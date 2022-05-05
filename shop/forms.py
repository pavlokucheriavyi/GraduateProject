from django import forms
from .models import Products
from django.views.generic import UpdateView

class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'myfield', 'placeholder': 'Пошук товара по назві'}), label='')


class RepairForm(forms.Form):
    FILTER_CHOICES = (
        ('some', '------------------'),
        ('bmw', 'bmw'),
        ('mersedes', 'mersedes'),
        ('audi', 'audi'),
    )

    name = forms.CharField(required=True, label='Ім`я')
    phone_number = forms.CharField(required=True, label='Номер телефону')
    marka_auto = forms.CharField(required=True, label='Номер телефону')
    model_auto = forms.CharField(required=True, label='Модель авто')
    type_of_repair = forms.CharField(required=True, label='Вид ремонту')