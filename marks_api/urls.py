from django.urls import path
from .views import MarksList

app_name = 'marks_api'

urlpatterns = [
    path('', MarksList.as_view(), name='checkmarks')
]