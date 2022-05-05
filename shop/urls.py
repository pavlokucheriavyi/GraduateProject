from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop', views.ProductsView.as_view(), name='shop'),
    path('shop/product/<int:pk>', views.product_detail, name='product_detail'),
    path('shop/product/<int:pk>/update', views.UpdateProductView.as_view(), name='update_product'),
    path('shop/product/<int:pk>/delete', views.DeleteProductView.as_view(), name='delete_product'),
    path('repair/<str:type_name>/', views.repair, name='repair_page'),
    path('filter-data', views.filter_data, name='filter_data')
]