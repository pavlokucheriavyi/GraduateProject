from django.urls import path, include
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.profile, name='profile'),
]