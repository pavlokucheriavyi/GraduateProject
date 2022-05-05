from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomAuthForm(forms.Form):
    username = forms.CharField(widget=TextInput(attrs={'class':'my_login_input','placeholder': 'Введіть логін або Email'}),
                               error_messages={'required': 'Please enter your login'}
                               )
    password = forms.CharField(widget=PasswordInput(attrs={'class':'my_login_input', 'placeholder':'Введіть пароль'}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=TextInput(attrs={'class': 'form-control','placeholder': 'Введіть Email'})
    )
    username = forms.CharField(
        required=True,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ім`я користувача'})

    )
    password1 = forms.CharField(
        required=True,
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль'})
    )
    password2 = forms.CharField(
        required=True,
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердіть пароль'})
    )

    User._meta.get_field('email')._unique = True

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

