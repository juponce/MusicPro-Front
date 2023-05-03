from django.shortcuts import render
from django.views.generic.base import TemplateView
from .services import get_product

# Create your views here.

def modificar_productos(request):
    template_name = "venta/productos.html"
    title = 'Productos'
    product = get_product()

    return render(request, template_name, {'title': title, 'product': product})


def products_page_view(request):
    template_name = "venta/catalogo.html"
    title = 'Catálogo'
    product = get_product()

    return render(request, template_name, {'title': title, 'product': product})

def carrito(request):
    if request.user.is_authenticated:
        user = request.user
        carrito, created = Carrito.objects.get_or_create(usuario=user)
        items = carrito.itemcarrito_set.all()
    else:
        items = []
        carrito = {'get_total_cart': 0}

    data = {'items': items, 'carrito': carrito, 'dona': dona}
    return render(request, 'venta/carrito.html', data)