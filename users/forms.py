from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'my_login_input','placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'my_login_input', 'placeholder':'Password'}))