# store/urls.py

from django.urls import path
from . import views

# app_name = 'store' # Namespace (opcional pero recomendado)

urlpatterns = [
    # Productos
    path('', views.product_list, name='product_list'),
    path('categoria/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('producto/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # Carrito
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('carrito/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('carrito/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # Pedidos
    path('pedido/crear/', views.order_create, name='order_create'),
    path('pedidos/', views.order_history, name='order_history'),
    # path('pedido/confirmacion/<int:order_id>/', views.order_confirmation, name='order_confirmation'), # Opcional
]