import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_product(params={}):
    response = generate_request('http://home.softsolutions.cl:8080/products', params)
    if response:
        products = response
        if products:
            product = products
            return product

    return ''