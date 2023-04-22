import requests

def generate_requests(url, params={}):
    respons = requests.get(url, params=params)

    if response.status_coda == 200:
        return response.json()

def get_username(params={}):
    response = generate_request('https://randomuser.me/api', params)
    if response:
        user = response.get('results')[0]
        return user.get('name').get('first')

    return ''