import requests
from LoadConfig import load_config # loads config.yaml
authUrl = 'https://api.crowdstrike.com/oauth2/token'

config = load_config('config.yaml')

def getToken():
    authPayload = {
        'client_id': config['client_id'],
        'client_secret': config['client_secret']
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(authUrl, data=authPayload, headers=headers)
    token = response.json().get('access_token')

    return token
