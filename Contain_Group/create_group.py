import requests
from GetToken import getToken

token = getToken()

# API URL
url = "https://api.crowdstrike.com/devices/entities/host-groups/v1"

assignment_rule = "hostname:*'DHC'*"

payload = {
    "resources": [
        {
            "name": "Containment Script Exclusion",
            "description": "Prevents DHCP servers from containing",
            "group_type": "dynamic",
            "assignment_rule": assignment_rule
        }
    ]
}

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, json=payload)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
