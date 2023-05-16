import requests
import random
from django.shortcuts import render
from django.http import HttpResponse
from transbank.webpay.webpay_plus.transaction import Transaction
from .models import *



def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_product(params={}):
    response = generate_request('http://home.softsolutions.cl:8080/productos', params)
    if response:
        products = response
        if products:
            product = products
            return product

    return ''

def get_product_by_id(id):
    response = generate_request('http://home.softsolutions.cl:8080/producto/'+ id)
    print('http://home.softsolutions.cl:8080/producto/'+ id)
    if response:
        products = response
        if products:
            product = products
            return product

    return ''

def delete_product_id(product_id):
    url = f"http://home.softsolutions.cl:8080/producto/{product_id}"
    print(url)
    response = requests.delete(url)
    if response.status_code == 204:
        print(response.status_code)
        return True
    else:
        return False

def delete_stock_id(stock_id):
    url = f"http://home.softsolutions.cl:8080/stock/{stock_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        print(response.status_code)
        return True
    else:
        return False

def delete_stock_by_product_id(product_id):
    url = f"http://home.softsolutions.cl:8080/stock/?id_producto={product_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        return True  # La eliminación se realizó correctamente
    else:
        return False  # Hubo un error al eliminar los registros de Stock

def get_bodegas(params={}):
    response = generate_request('http://home.softsolutions.cl:8080/bodegas', params)
    if response:
        products = response
        if products:
            product = products
            return product

    return ''

def get_stocks(params={}):
    response = generate_request('http://home.softsolutions.cl:8080/stocks', params)
    if response:
        stocks = response
        if stocks:
            stock = stocks
            return stock

    return ''


# Host: hhttps://webpay3gint.transbank.cl/

# tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))

## Versión 2.x del SDK
# El SDK apunta por defecto al ambiente de pruebas, no es necesario configurar lo siguiente
# transbank.webpay.webpay_plus.webpay_plus_default_commerce_code = 597055555532
# transbank.webpay.webpay_plus.default_api_key = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
# transbank.webpay.webpay_plus.default_integration_type = IntegrationType.TEST

def webpay_plus_create(request):
    user = request.user
    carrito, created = Carrito.objects.get_or_create(usuario=user)
    items = carrito.itemcarrito_set.all()
    total = 0
    print(items)
    for i in items:
        total =total + (i.precio * i.cantidad)
        print(total)

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

    response = (Transaction()).create(buy_order, session_id, amount, return_url)

    print(response)

    return render(request, 'venta/exito.html', {'request': create_request, 'response': response})

# def webpay_plus_commit(request):
#     token = request.GET.get("token_ws")
#     print("commit for token_ws: {}".format(token))

#     response = (Transaction()).commit(token=token)
#     print("response: {}".format(response))

#     return render(request, 'venta/commit.html', {'token': token, 'response': response})

# tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
# resp = tx.create(buy_order, session_id, amount, return_url)