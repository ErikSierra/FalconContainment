import requests
#to get device id froma host name
def getDeviceId(token, hostname):
    url = "https://api.crowdstrike.com/devices/queries/devices/v1"
    headers = {
        "Authorization": f"Bearer {token}"
        }
    params = {
        "filter": f"hostname:'{hostname}'"
        }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    devices = response.json()["resources"]
    return devices[0] if devices else None