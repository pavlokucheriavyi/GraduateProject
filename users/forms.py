from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .token import token_generator

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

    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string(
            'users/activate_account.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
        )

        # send_mail(subject, message, 'kobra1903@ukr.net', ['test-ykf0q4akt@srv1.mail-tester.com'], html_message=message, fail_silently=True)

        user.email_user(subject, message, html_message=message)


class UpdatePasswordForm(UserCreationForm):
    password1 = forms.CharField(
        required=True,
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль'})
    )
    password2 = forms.CharField(
        required=True,
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердіть пароль'})
    )

    class Meta:
        model = User
        fields = ['password1', 'password2']


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


