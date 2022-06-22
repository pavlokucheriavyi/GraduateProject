"""kolischa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as vws
from users.forms import CustomAuthForm
from django.contrib.auth import views as auth_views
from users.views import (ActivateView,
                         CheckEmailView,
                         SuccessView,
                         login,
                         registration,
                         reset_password)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('profile', include('users.urls', namespace='profile')),
    path('', include('shop.urls')),
    path('captcha/', include('captcha.urls')),
    path('api/', include('marks_api.urls')),
    path('logIn/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('exit', vws.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name="activate"),
    path('check-email/', CheckEmailView.as_view(), name="check_email"),
    path('success/', SuccessView.as_view(), name="success"),
    path('reset_password/', reset_password, name="reset_password"),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name='users/reset_password_done.html'), name='reset_password_done'),
    path('reset_password_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/reset_password_confirm.html"), name='reset_password_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_password_complete.html'), name='password_reset_complete'),

]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
