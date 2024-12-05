import requests
import os
import yaml
import sys
authUrl = 'https://api.crowdstrike.com/oauth2/token'

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

# Function to load configuration
def load_config(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: Configuration file '{file_path}' not found.")
        sys.exit(1)

    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
            return config
    except yaml.YAMLError as e:
        print(f"Error reading configuration file: {e}")
        sys.exit(1)


config = load_config('config.yaml')
