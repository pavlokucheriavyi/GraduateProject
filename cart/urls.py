from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('success', views.cart_delete_all, name='cart_delete_all'),
    path('add/<int:product_id>', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('take_order', views.take_order, name='take_order'),
    path('test_url/', views.test_view, name='test_view')
]
