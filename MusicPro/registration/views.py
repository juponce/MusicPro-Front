# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpFormWithEmail
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.

# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     template_name = 'registration/signup.html'

#     def get_success_url(self):
#         return reverse_lazy('login') + '?register'

class SignUpView(CreateView):
    form_class = SignUpFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('signin') + '?register'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        data = {
            'name': name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password
        }

        response = requests.post('https://api.example.com/login', data=data)

        if response.status_code == 200:

            print('Inicio de sesión exitoso en la API')
        else:

            print('Error al iniciar sesión en la API')

        return super().form_valid(form)

    
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        data = {
            'email': email,
            'password': password
        }
        response = requests.post('https://api.example.com/login', data=data)

        if response.status_code == 200:
    
            print('Inicio de sesión exitoso en la API')
        else:
    
            print('Error al iniciar sesión en la API')

    return render(request, 'registration/login.html')