from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop', views.ProductsView.as_view(), name='shop'),
    path('shop/product/<int:pk>', views.ProductDetailView.as_view(), name='product_detail')
]