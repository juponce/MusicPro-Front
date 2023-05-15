import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_product(params={}):
    response = generate_request('http://home.softsolutions.cl:8080/productos', params)
    if response:
        products = response
        if products:
            product = products
            return product

    return ''

def get_product_by_id(id):
    response = generate_request('http://home.softsolutions.cl:8080/producto/'+ id)
    print('http://home.softsolutions.cl:8080/producto/'+ id)
    if response:
        products = response
        if products:
            product = products
            return product

    return ''

def delete_product_id(product_id):
    url = f"http://home.softsolutions.cl:8080/producto/{product_id}"
    print(url)
    response = requests.delete(url)
    if response.status_code == 204:
        print(response.status_code)
        return True
    else:
        return False

def delete_stock_id(stock_id):
    url = f"http://home.softsolutions.cl:8080/stock/{stock_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        print(response.status_code)
        return True
    else:
        return False

def delete_stock_by_product_id(product_id):
    url = f"http://home.softsolutions.cl:8080/stock/?id_producto={product_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        return True  # La eliminación se realizó correctamente
    else:
        return False  # Hubo un error al eliminar los registros de Stock

def get_bodegas(params={}):
    response = generate_request('http://home.softsolutions.cl:8080/bodegas', params)
    if response:
        products = response
        if products:
            product = products
            return product

    return ''

def get_stocks(params={}):
    response = generate_request('http://home.softsolutions.cl:8080/stocks', params)
    if response:
        stocks = response
        if stocks:
            stock = stocks
            return stock

    return ''



