from django.urls import path
from .views import *

urlpatterns = [
    path('', products_page_view, name="catalogo"),
    path('carrito/', carrito, name='carrito'),
    path('anadir_producto/', anadir_producto, name='anadir_producto'),
    path('stock/<str:content>/', stock_view, name='stock'),
    path('modificar_productos', modificar_productos, name='modificar_productos'),
    path('productos/eliminar/', eliminar_producto, name='eliminar_producto'),
    path('update_carrito/', update_carrito, name='update_carrito'),
    path('actualizar-producto/<int:producto_id>/', editar_producto, name='actualizar-producto'),

]