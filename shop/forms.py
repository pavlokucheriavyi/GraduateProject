from django import forms
from .models import Products
from django.views.generic import UpdateView


class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'myfield', 'placeholder': 'Пошук товара по назві'}), label='')

