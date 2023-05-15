import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .services import *
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib import messages


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


# def login_view(request):
#     user = get_users()
#     if request.method == 'POST':
#         correo  = request.POST.get('email')
#         contrasena = request.POST.get('password')

#         for i in user:
#             if email == i.get('correo') and password == i.get('contrasena'):
#                 user_login = authenticate(request, username=i.get('nombre'), password=i.get('contrasena'))

#                 if user is not None:
#                     login(request, user_login)
#                     return redirect('home')
#             else:
#                 print(i.get('correo'))
#                 print(email)
#                 print(i.get('contrasena'))
#                 print("NOOOO")

#     return render(request, 'registration/login.html')

def login_view(request):
    if request.method == 'POST':
        correo = request.POST['email']
        contrasena = request.POST['password']
        
        if verificar_credenciales(correo, contrasena):
            crear_usuario(correo, contrasena)
            messages.success(request, 'Usuario creado correctamente.')
            user = authenticate(username=correo, password=contrasena)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas.')

    return render(request, 'registration/login.html')