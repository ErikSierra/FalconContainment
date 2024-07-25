import requests

#removes admin rights
def removeAdminRights(token, session_id, username):
    url = "https://api.crowdstrike.com/real-time-response/entities/execute-command/v1"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "base_command": "runscript",
        "command_string": f"Remove-LocalGroupMember -Group \"Administrators\" -Member \"{username}\"",
        "session_id": session_id
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
