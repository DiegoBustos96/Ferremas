# store/cart.py

from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        """
        Inicializa el carrito.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Guarda un carrito vacío en la sesión
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Añade un producto al carrito o actualiza su cantidad.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Marca la sesión como "modificada" para asegurarte de que se guarde
        self.session.modified = True

    def remove(self, product):
        """
        Elimina un producto del carrito.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Itera sobre los artículos en el carrito y obtiene los productos
        de la base de datos.
        """
        product_ids = self.cart.keys()
        # Obtiene los objetos product y los añade al carrito
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Cuenta todos los artículos en el carrito.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Elimina el carrito de la sesión
        del self.session[settings.CART_SESSION_ID]
        self.save()

# Añade esta línea en ferremas/settings.py para definir la clave de sesión del carrito
# CART_SESSION_ID = 'cart'