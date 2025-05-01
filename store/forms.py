# store/forms.py

from django import forms
from .models import Order

# Opciones de cantidad para el formulario de añadir al carrito
QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)] # Cantidad de 1 a 10

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=QUANTITY_CHOICES,
        coerce=int,
        label='Cantidad',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    # Campo oculto para indicar si se debe sobrescribir la cantidad existente o añadir
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle, número, depto'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal (opcional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'address': 'Dirección de Envío',
            'postal_code': 'Código Postal',
            'city': 'Ciudad',
        }