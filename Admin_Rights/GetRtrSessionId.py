import requests

#intiates real time responsive session
def initiateRtrSession(token, device_id):
    url = "https://api.crowdstrike.com/real-time-response/entities/sessions/v1"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "device_id": device_id
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["resources"][0]["session_id"]