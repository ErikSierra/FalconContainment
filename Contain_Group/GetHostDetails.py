import requests
import json
# Constants
CLOUD_BASE_URL = "https://api.crowdstrike.com"
CLIENT_ID = ""      # Replace with your actual Client ID
CLIENT_SECRET = "" # Replace with your actual Client Secret

# Step 1: Authenticate to get the OAuth token
auth_url = f"{CLOUD_BASE_URL}/oauth2/token"
auth_data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}

auth_response = requests.post(auth_url, data=auth_data)
auth_response.raise_for_status()  # Raise an error for bad status codes
auth_token = auth_response.json()['access_token']

# Step 2: Get host details
headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json'
}

# Replace with actual host IDs (maximum 100 for GET or 5000 for POST)
host_ids = [""]

# Making a POST request to fetch details for multiple hosts
details_url = f"{CLOUD_BASE_URL}/devices/entities/devices/v2"
payload = {
    'ids': host_ids
}

response = requests.post(details_url, headers=headers, json=payload)
response.raise_for_status()  # Raise an error for bad status codes

# Get the host details
host_details = response.json()

# Print the host details in a formatted way
print(json.dumps(host_details, indent=4))


# Write the host details to a text file in a formatted way
# with open("host_details.txt", "w") as file:
#     file.write(json.dumps(host_details, indent=4))

# print("Host details have been written to host_details.txt")
