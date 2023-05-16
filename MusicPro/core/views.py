from django.shortcuts import render
from django.views.generic.base import TemplateView
from transbank.webpay.webpay_plus.transaction import Transaction

# Create your views here.

class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'Inicio'})

def webpay_plus_commit(request):
    token = request.GET.get('token_ws')
    print("commit for token_ws: {}".format(token))

    response = (Transaction()).commit(token=token)
    print("response: {}".format(response))

    return render(request, 'core/exito.html', {'token': token, 'response': response})