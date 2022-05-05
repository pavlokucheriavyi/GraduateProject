from django.shortcuts import render, redirect

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from users.forms import CustomAuthForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import CustomAuthForm
from .forms import RegisterForm
from .decorators import anonymous_required


def login(request):
    if request.method == 'POST':
        form = CustomAuthForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            print(data)
            if user:
                auth_login(request, user)
                messages.success(request, f'Ласкаво просимо, {user}')
                return redirect('home')
            else:
                messages.error(request, 'Невірно вказано логін або пароль, спробуйте ще раз')
                return redirect('login')
    else:
        form = CustomAuthForm()
    context = {'form': form}

    return render(request, 'users/user.html', context)


@anonymous_required(redirect_url='home')
def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Користувач {user} успішно зареєстрований, виконайте вхід')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/registration.html', {'form': form})



