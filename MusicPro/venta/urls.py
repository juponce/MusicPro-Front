from django.urls import path
from .views import *

urlpatterns = [
    path('', products_page_view, name="catalogo"),
    path('carrito/', carrito, name='carrito'),
]