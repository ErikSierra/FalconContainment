import requests
from GetToken import getToken
    
token = getToken()

url = "https://api.crowdstrike.com/devices/entities/host-groups/v1"

assignment_rule = '{"AND":[{"operator":"contains","value":"DHC","field":"hostname"}]}'

payload = {
    "resources": [
        {
            "name": "Containment Script Exclusion",
            "description": "includes all servers to prevent from containing",
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

print(response.status_code)
print(response.json())
