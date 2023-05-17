from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from venta.models import *
import requests

# @receiver(user_logged_out)
# def eliminar_usuario(sender, user, request, **kwargs):
#     if not user.is_superuser:
#         url_carrito = 'http://home.softsolutions.cl:8080/carrito'
#         url_detalle = 'http://home.softsolutions.cl:8080/carritoDetalle'
#         carrito, created = Carrito.objects.get_or_create(usuario=user)
#         items = carrito.itemcarrito_set.all()
#         data_venta = {
#         'correo': user.username,
#         }

#         response_carrito = requests.post(url_carrito, data=data_venta)
#         carrito_id = int(response_carrito.text)
#         print(carrito_id)

#         if response_carrito.status_code == 200:
#             for i in items:
#                 data_detalle = {
#                     'cantidad': i.cantidad,
#                     'id_producto': i.id_producto,
#                     'id_carrito': carrito_id,
#                     }
#                 response_detalle = requests.post(url_detalle, data=data_detalle)
#                 if response_detalle.status_code == 200:
#                     print('funciono!!')
#                 else:
#                     print(response_detalle.text)
#                     print(i.id_producto)
#                     print('no funciono')

#         if response_carrito.status_code == 200 and response_detalle.status_code == 200:
#             for i in items:
#                 i.delete()
#             carrito.delete()

#             User.objects.filter(id=user.id).delete()

@receiver(user_logged_out)
def eliminar_usuario(sender, user, request, **kwargs):
    if not user.is_superuser:
        User.objects.filter(id=user.id).delete()