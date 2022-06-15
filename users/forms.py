from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Cars


class CustomAuthForm(forms.Form):
    email = forms.CharField(
        widget=TextInput(attrs={'class': 'my_login_input', 'placeholder': 'Введіть будь-ласка ваш email'}),
        error_messages={'required': 'Please enter your email'}
    )
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'my_login_input', 'placeholder': 'Введіть пароль'}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть Email'})
    )
    first_name = forms.CharField(
        required=True,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ім`я'})
    )
    last_name = forms.CharField(
        required=True,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть прізвище'})
    )
    username = forms.CharField(
        required=True,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть логін'})
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
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        label='',
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ім`я'})
    )

    last_name = forms.CharField(
        required=True,
        label='',
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть прізвище'})
    )

    username = forms.CharField(
        required=True,
        label='login',
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть login'})
    )

    email = forms.EmailField(
        required=True,
        label='email',
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть email'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UserImageForm(forms.ModelForm):
    img = forms.ImageField(
        required=False,
        label='Завантажити фото'
    )

    class Meta:
        model = Profile
        fields = ['img']


class CarImageForm(forms.ModelForm):
    img_of_avto = forms.ImageField(
        required=False,
        label='Завантажити фото'
    )

    class Meta:
        model = Cars
        fields = ['img_of_avto']


