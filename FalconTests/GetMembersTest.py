from falconpy import Hosts

# Enable pythonic responses when you construct an instance of the class
hosts = Hosts(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, pythonic=True)

# Define the group name to filter by
group_name = 'Workflow Testing'

# Construct the filter
filter = f"falcon_sandbox_id:{hosts.creds.sandbox_id} AND group_name:'{group_name}'"

# Query devices by the filter and loop through the results
result = hosts.query_devices_by_filter_scroll(filter=filter)
if not result.raw:
    for device_id in result:
        print(device_id)