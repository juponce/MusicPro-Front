from django.shortcuts import render
from django.views.generic.base import TemplateView
from transbank.webpay.webpay_plus.transaction import Transaction
from venta.models import *
import requests

# Create your views here.

class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'Inicio'})

def webpay_plus_commit(request):
    user = request.user
    carrito, created = Carrito.objects.get_or_create(usuario=user)
    items = carrito.itemcarrito_set.all()
    total = 0
    correo = user.username
    token = request.GET.get('token_ws')
    # print("commit for token_ws: {}".format(token))

    response = (Transaction()).commit(token=token)
    # print("response: {}".format(response))

    for i in items:
        total =total + (i.precio * i.cantidad)


    if request.user.is_authenticated:
        url_venta = 'http://home.softsolutions.cl:8080/venta'
        url_detalle = 'http://home.softsolutions.cl:8080/ventadetalle'
        orden = response['buy_order']
        data_venta = {
        'total_venta': total,
        'orden_compra': orden,
        'correo': correo,
        }



        response_venta = requests.post(url_venta, data=data_venta)
        venta_id = response_venta.json()
        print(venta_id)
        print(type(venta_id))
        print(venta_id["idVenta"])
        print(type(venta_id["idVenta"]))

        if response_venta.status_code == 200:

            for i in items:
                data_detalle = {
                'cantidad': i.cantidad,
                'id_producto': i.id_producto,
                'id_venta': venta_id["idVenta"],
                }
                response_detalle = requests.post(url_detalle, data=data_detalle)
                if response_detalle.status_code == 200:
                    print('funciono!!')
                else:
                    print(response_detalle.text)
                    print(i.id_producto)
                    print('no funciono')

        if response_venta.status_code == 200 and response_detalle.status_code == 200:
            for i in items:
                i.delete()
            carrito.delete()

    return render(request, 'core/exito.html', {'token': token, 'response': response})