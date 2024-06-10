from falconpy.hosts import Hosts

falcon_auth = { 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET }
falcon = Hosts(creds=falcon_auth)

# Define filter to retrieve all hosts in group
group_id = 'ac71d7e8c876456eb10424ca96f2049d'
filter = f"group_id:'{group_id}'"
devices = falcon.query_devices_by_filter(filter=filter)

print(devices['resources'])