

from falconpy.hosts import Hosts

# Replace GROUP_ID with the ID of the group you want to query
GROUP_ID = "my-group-id"

# Create a Hosts instance and authenticate
falcon = Hosts(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Query devices by group ID
devices = falcon.query_devices_by_filter(filter=f"group_id:'{GROUP_ID}'", sort="hostname.asc")

# Print the results
print(devices)