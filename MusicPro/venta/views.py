import random
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from .services import *
import requests
from .models import *
from django.urls import reverse
from django.http import JsonResponse
import json
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction

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
            id_producto = response.json()
            print(id_producto["id_producto"])
            return redirect('stock', content = id_producto["id_producto"])
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
    # items = None
    # carrito = None
    # total = None
    if request.user.is_authenticated:
        
        user = request.user
        carrito, created = Carrito.objects.get_or_create(usuario=user)
        items = carrito.itemcarrito_set.all()
        total = 0
        print(items)
        for i in items:
            total =total + (i.precio * i.cantidad)
            print(total)

        # valor_dolares = usd_convert(1000)

        print("Webpay Plus Transaction.create")
        buy_order = str(random.randrange(1000000, 99999999))
        session_id = str(random.randrange(1000000, 99999999))
        amount = total
        return_url = request.build_absolute_uri('/webpay-plus/commit')

        create_request = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": amount,
            "return_url": return_url
        }
        
        if amount != 0:
            valor_dolares = round(usd_convert(total), 2)
            response = (Transaction()).create(buy_order, session_id, amount, return_url)

            print(response['token'])
            print(response['url'])

        # tarjeta de prueba 	4051 8856 0044 6623
        
            data = {
                'items': items,
                'carrito': carrito,
                'total': total,
                'token_ws': response['token'],
                'url': response['url'],
                'dolar': valor_dolares,
                }
            
            return render(request, 'venta/carrito.html', data)
        
        data = {
            'items': items,
            'carrito': carrito,
            'total': total,
            'dolar': 0,
            }

        return render(request, 'venta/carrito.html', data)

def webpay_plus_commit(request):
    token_ws = request.GET.get('token_ws')
    print(token_ws)
    print("commit for token_ws: {}".format(token))

    response = (Transaction()).commit(token=token_ws)
    print("response: {}".format(response))

    return render(request, 'venta/exito.html', {'token': token, 'response': response})

def retorno_webpay(request):
    token_ws = request.POST.get('token_ws')

    transaction = webpay.Transaction.status(token_ws)
    if transaction.status == 'AUTHORIZED':
        return render(request, 'webpay/exito.html')
    else:
        return render(request, 'webpay/error.html')

def stock_view(request, content):
    bodegas = get_bodegas()
    product = get_product_by_id(content)
    stocks = get_stocks()
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

        
        for i in stocks:
            if i['id_producto'] == id_producto:
                url = url + '/' + str(i['id_stock'])
                response = requests.put(url, data)
                if response.status_code == 200:
                    return redirect('anadir_producto')
                else:
                    print('esta', cantidad)
                    print(id_producto)
                    print('bodega',bodega)
                    print(response.status_code)

        response = requests.post(url, data=data)

        if response.status_code == 200:
            return redirect('anadir_producto')
        else:
            print('esta', cantidad)
            print(id_producto)
            print('bodega',bodega)
            print(response.status_code)
    return render(request, 'venta/stock.html', {'product': product, 'bodegas': bodegas })


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

def editar_producto(request, producto_id):
    producto = get_product_by_id(producto_id)
    producto_editable = producto[0]
    print(producto_editable['nombre'])
    id_str = str(producto_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        imagen = request.POST.get('imagen')

        url = 'http://home.softsolutions.cl:8080/producto/' + id_str
        data = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'imagen': imagen,
            'cantidad': 3,
        }

        print(data)

        response = requests.put(url, data=data)

        if response.status_code == 200:
            return redirect('stock', content = producto_id)
        else:
            # manejar errores
            print(response.status_code)
            print(response.content)
    

    context = {
        'producto': producto_editable
    }
    
    return render(request, 'venta/anadir_producto.html', context)

def historial_view(request):
    template_name = "venta/historial.html"
    title = 'Historial'
    ventas = get_ventas()
    ventasUsuario = []
    email = request.user.username

    for i in ventas:
        if i['correo'] == email:
            ventasUsuario.append(i)

    print(ventasUsuario)
    
    return render(request, template_name, {'title': title, 'ventasUsuario': ventasUsuario})

def detalle_view(request, detalle_id):
    template_name = "venta/detalle.html"
    title = 'Detalle'
    detalle = get_detalles()
    product = get_product()
    detalleVenta = []

    for i in detalle:
        print(i)
        if i['id_venta'] == detalle_id:
            for n in product:
                print(n)
                if n['id_producto'] == i['id_producto']:
                    detalleVenta.append(n)

    print(detalleVenta)

    # for i in ventas:
    #     if i['correo'] == email:
    #         ventasUsuario.append(i)

    # print(ventasUsuario)
    
    return render(request, template_name, {'title': title, 'detalleVenta': detalleVenta})