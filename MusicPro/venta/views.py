from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class ProductsPageView(TemplateView):
    template_name = "venta/productos.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'productos'})