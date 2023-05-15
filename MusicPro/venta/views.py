from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from .services import *
import requests
from .models import *
from django.urls import reverse
from django.http import JsonResponse
import json

# Create your views here.

def modificar_productos(request):
    template_name = "venta/productos.html"
    title = 'Productos'
    product = get_product()
    stocks = get_stocks()
    stocks_delete = []

    if request.method == 'POST':
        product_id = request.POST['product_id']
        for i in stocks:
            if i.get('id_producto') == int(product_id):
                stocks_delete.append(i)
        for i in stocks_delete:
            id_stock = i.get('id_stock')
            if delete_stock_id(id_stock):
                pass
            else:
                pass
    
        if delete_product_id(product_id):
            pass
        else:
            print(product_id)
            return redirect('modificar_productos')

    return render(request, template_name, {'title': title, 'product': product})


def anadir_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        imagen = request.POST.get('imagen')

        url = 'http://home.softsolutions.cl:8080/producto'
        data = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'imagen': imagen,
            'cantidad': 3,
        }

        response = requests.post(url, data=data)
        # print(type(response.status_code))


        if response.status_code == 200:
            id_producto = response.text

            return redirect('stock', content = id_producto)
        else:
            # manejar errores
            print(response.status_code)

    return render(request, 'venta/anadir_producto.html')


def products_page_view(request):
    template_name = "venta/catalogo.html"
    title = 'Catálogo'
    product = get_product()

    if request.user.is_authenticated:
        user = request.user
        carrito, created = Carrito.objects.get_or_create(usuario=user)
        items = carrito.itemcarrito_set.all()
    else:
        items = []

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        producto = request.POST.get('producto')
        carrito_id = carrito
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')
        item_carrito = ItemCarrito(id_producto=product_id, producto=producto, carrito=carrito_id, cantidad=cantidad, precio=precio)
        item_carrito.save()
        print("al menos lees esto")
    

    return render(request, template_name, {'title': title, 'product': product})

def eliminar_producto(request):
    return render(request, 'venta/productos.html')

def carrito(request):
    if request.user.is_authenticated:
        user = request.user
        carrito, created = Carrito.objects.get_or_create(usuario=user)
        items = carrito.itemcarrito_set.all()

    data = {'items': items, 'carrito': carrito}
    return render(request, 'venta/carrito.html', data)

def stock_view(request, content):
    bodegas = get_bodegas()
    product = get_product_by_id(content)
    if request.method == 'POST':
        cantidad = request.POST.get('stock')
        id_producto = int(content)
        bodega = request.POST.get('bodega')
        print(cantidad)
        print(id_producto)
        print(bodega)

        url = 'http://home.softsolutions.cl:8080/stock'
        data = {
            'cantidad': cantidad,
            'id_producto': id_producto,
            'id_bodega': bodega,           
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            return redirect('anadir_producto')
        else:
            # manejar errores
            print('esta', cantidad)
            print(id_producto)
            print('bodega',bodega)
            print(response.status_code)
    return render(request, 'venta/stock.html', {'product': product, 'bodegas': bodegas })

# def update_carrito(request):
#     user = request.user
#     carrito, created = Carrito.objects.get_or_create(usuario=user)
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         action = request.POST.get('action')

#         print(product_id)
#         print(action)
#         # Realiza la lógica para incrementar la cantidad del registro ItemCarrito según el product_id y action

#         # Actualiza la cantidad en el registro
#         item = ItemCarrito.objects.get(id_producto=product_id, carrito=carrito)
#         if action == 'add':
#             item.cantidad += 1
#         elif action == 'remove':
#             item.cantidad -= 1

#         item.save()

#         # Devuelve la nueva cantidad en la respuesta JSON
#         response_data = {
#             'cantidad': item.cantidad
#         }

#         return JsonResponse(response_data)

#     return JsonResponse({'error': 'Invalid request'})

def update_carrito(request):
    stock = get_stocks()

    user = request.user
    carrito, created = Carrito.objects.get_or_create(usuario=user)

    data =json.loads(request.body)

    productId = data['product_id']
    action = data['action']

    stock_max = 100

    for i in stock:
        if i.get('id_producto') == int(productId):
            print('se asigno')
            stock_max = i.get('cantidad')

    itemCarrito, created = ItemCarrito.objects.get_or_create(carrito=carrito, id_producto=productId)

    print('productId:', productId)
    print('Action:', action)
    print('stock_max:', stock_max)
    print('itemCarrito.cantidad:', itemCarrito.cantidad)


    if action == 'add' and stock_max > itemCarrito.cantidad:
        itemCarrito.cantidad = (itemCarrito.cantidad + 1)
    elif action == 'remove':
        itemCarrito.cantidad = (itemCarrito.cantidad - 1)
    elif action == 'delete':
        itemCarrito.cantidad = 0
    
    itemCarrito.save()

    if itemCarrito.cantidad <= 0:
        itemCarrito.delete()
    return JsonResponse('Producto añadido', safe=False)