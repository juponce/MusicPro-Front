import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


def signup_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        contrasena = request.POST.get('contrasena')
        tipo_cuenta = request.POST.get('tipo_cuenta')

        url = 'http://home.softsolutions.cl:8080/usuario'
        data = {
            'correo': correo,
            'nombre': nombre,
            'apellido': apellido,
            'contrasena': contrasena,
            'tipo_cuenta': tipo_cuenta,
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            return redirect('signup')
        else:
            # manejar errores
            pass

    return render(request, 'registration/signup.html')


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