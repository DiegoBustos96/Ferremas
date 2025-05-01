# store/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Order, OrderItem
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'store/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # Formulario para añadir al carrito (se inicializa aquí para mostrarlo en la página)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'store/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

@require_POST # Solo permite peticiones POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # Verifica si hay stock suficiente
        current_quantity_in_cart = cart.cart.get(str(product_id), {}).get('quantity', 0)
        requested_quantity = cd['quantity']
        # Si actualiza, la cantidad total es la nueva. Si añade, es la suma.
        total_requested = requested_quantity if cd['update'] else current_quantity_in_cart + requested_quantity

        if product.stock >= total_requested:
             cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
             messages.success(request, f'"{product.name}" añadido/actualizado en tu carrito.')
        else:
            messages.error(request, f'No hay suficiente stock para "{product.name}". Disponible: {product.stock}.')

    else:
         messages.error(request, 'Error al añadir el producto. Inténtalo de nuevo.')
    # Redirige a la URL desde la que se añadió el producto (o al carrito si no hay referrer)
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'"{product.name}" eliminado de tu carrito.')
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    # Añadir formulario de actualización de cantidad a cada item del carrito
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True # Importante: marca que es una actualización
        })
    return render(request, 'store/cart/detail.html', {'cart': cart})

@login_required # Requiere que el usuario esté logueado para el checkout
def order_create(request):
    cart = Cart(request)
    if not cart: # Si el carrito está vacío, redirigir
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user # Asigna el usuario logueado
            order.save() # Guarda el pedido principal

            # Variable para verificar stock
            stock_ok = True
            products_to_update = []

            for item in cart:
                product_instance = item['product']
                quantity_ordered = item['quantity']

                # Verificar stock ANTES de crear OrderItem
                if product_instance.stock < quantity_ordered:
                    messages.error(request, f'No hay suficiente stock para "{product_instance.name}". Disponible: {product_instance.stock}. Por favor, ajusta tu carrito.')
                    stock_ok = False
                    break # Salir del bucle si un producto no tiene stock
                else:
                    OrderItem.objects.create(order=order,
                                             product=product_instance,
                                             price=item['price'],
                                             quantity=quantity_ordered)
                    # Guardar el producto y la cantidad a descontar
                    product_instance.stock -= quantity_ordered
                    products_to_update.append(product_instance)

            if stock_ok:
                # Si todo el stock está OK, actualizar la base de datos
                Product.objects.bulk_update(products_to_update, ['stock']) # Actualiza stock eficientemente

                # Limpia el carrito
                cart.clear()
                messages.success(request, '¡Tu pedido ha sido creado con éxito!')

                # Aquí es donde normalmente redirigirías a la pasarela de pago
                # Como las APIs están excluidas, vamos a una página de confirmación simple
                # Puedes pasar el ID del pedido a la página de confirmación si es necesario
                # return redirect('order_confirmation', order_id=order.id) # Si creas esta URL/Vista
                return render(request, 'store/order/created.html', {'order': order})
            else:
                # Si hubo error de stock, el pedido principal ya se creó pero sin items.
                # Podrías borrar el 'order' aquí o manejarlo de otra forma.
                # Por simplicidad, solo mostramos el error y el usuario debe volver al carrito.
                 order.delete() # Borramos el pedido vacío creado
                 return redirect('cart_detail')


    else: # Método GET
        # Pre-rellenar datos si el usuario está logueado (opcional)
        initial_data = {}
        if request.user.is_authenticated:
             initial_data = {
                 'first_name': request.user.first_name,
                 'last_name': request.user.last_name,
                 'email': request.user.email,
                 # Podrías tener un perfil de usuario con dirección, etc.
             }
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'store/order/create.html', {'cart': cart, 'form': form})



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items', 'items__product')
    return render(request, 'store/order/history.html', {'orders': orders})
