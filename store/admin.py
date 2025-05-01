# store/admin.py

from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # Autocompleta slug basado en name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at', 'category']
    list_editable = ['price', 'stock', 'available'] # Permite editar estos campos en la lista
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

class OrderItemInline(admin.TabularInline): # Para mostrar items dentro del pedido
    model = OrderItem
    raw_id_fields = ['product'] # Mejora la selección de producto si hay muchos
    extra = 0 # No mostrar items vacíos por defecto

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'address', 'paid', 'created_at']
    list_filter = ['paid', 'created_at', 'updated_at']
    search_fields = ['id', 'first_name', 'last_name', 'email']
    inlines = [OrderItemInline] # Muestra los items del pedido