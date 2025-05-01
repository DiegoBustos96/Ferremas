# store/models.py

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=100, unique=True, help_text="Versión amigable para URL, ej: herramientas-manuales")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Categoría")
    name = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(max_length=200, unique=True, help_text="Versión amigable para URL, ej: martillo-carpintero-modelo-x")
    description = models.TextField(blank=True, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Precio") # Usar DecimalField para precios
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, verbose_name="Imagen") # Necesita Pillow: pip install Pillow

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario") # Puede ser null si es compra anónima
    first_name = models.CharField(max_length=50, verbose_name="Nombre")
    last_name = models.CharField(max_length=50, verbose_name="Apellido")
    email = models.EmailField(verbose_name="Correo Electrónico")
    address = models.CharField(max_length=250, verbose_name="Dirección")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Código Postal")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    paid = models.BooleanField(default=False, verbose_name="Pagado") # Simple indicador, la lógica de pago real iría aquí (API)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'Pedido {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Pedido")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="Producto")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Precio")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    class Meta:
        verbose_name = "Artículo de Pedido"
        verbose_name_plural = "Artículos de Pedido"

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity