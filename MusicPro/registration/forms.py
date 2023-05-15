from django import forms
from django.contrib.auth.models import User
from .services import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

def crear_usuario(correo, contrasena):
    tipo_cuenta = obtener_tipo_cuenta(correo)

    if tipo_cuenta:
        # Utiliza el correo electrónico como nombre de usuario
        username = correo

        # Verifica si el usuario ya existe en Django
        if User.objects.filter(username=username).exists():
            return False

        # Crea el usuario en Django
        user = User.objects.create_user(username=username, password=contrasena)
        user.user_type = tipo_cuenta
        user.save()
        if tipo_cuenta == 1:
            group = Group.objects.get(name='admin')
            user.groups.add(group)
        elif tipo_cuenta == 2:
            group = Group.objects.get(name='cliente')
            user.groups.add(group)
            print("cliente creado")

        return True
    else:
        return False
