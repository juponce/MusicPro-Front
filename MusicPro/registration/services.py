import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_users(params={}):
    response = generate_request('http://home.softsolutions.cl:8080/usuarios', params)
    if response:
        users = response
        if users:
            user = users
            return user

    return ''

def verificar_credenciales(correo, contrasena):
    url = 'http://home.softsolutions.cl:8080/usuarios'
    response = requests.get(url)
    
    if response.status_code == 200:
        usuarios = response.json()
        for usuario in usuarios:
            if usuario['correo'] == correo and usuario['contrasena'] == contrasena:
                return True
        return False
    else:
        return False

def obtener_tipo_cuenta(correo):
    url = f'http://home.softsolutions.cl:8080/usuario/{correo}'
    response = requests.get(url)
    
    if response.status_code == 200:
        usuario = response.json()
        tipo_cuenta = response.json()[0].get('tipo_cuenta')
        return tipo_cuenta
    else:
        return None

# tipo_cuenta = obtener_tipo_cuenta('cliente@cliente.com')

# def obtener_carrito(correo):
#     url_carrito = f'http://home.softsolutions.cl:8080/carrito/{correo}'
#     response = requests.get(url_carrito)

#     if response.status_code == 200:
#         carrito_json = response.json()
#         tipo_cuenta = carrito_json['id_carrito']
#         url_detalle = 'http://home.softsolutions.cl:8080/carritosDetalle'

#         response_detalle = requests.get(url_detalle)

#         if response.status_code == 200:
#             print(response_detalle)
#     else:
#         return None

    