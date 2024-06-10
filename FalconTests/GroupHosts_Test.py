import json
from falconpy import HostGroup, Hosts, APIHarness

CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
GROUP_ID = 'ac71d7e8c876456eb10424ca96f2049d'

falcon = APIHarness(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)


def list_host_group_members(group_id):
    try:
        host_group = HostGroup(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        
        response = host_group.query_group_members(limit=5000, id=group_id)
        if response['status_code'] != 200:
            print(f"Error fetching group members: {response['errors']}")
            return
        
        host_ids = response['body']['resources']
        if not host_ids:
            print("No hosts found in the group.")
            return
        
        # Fetch details for each host
        hosts = Hosts(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        host_details = hosts.get_device_details(ids=host_ids)
        
        # Print the details of each host
        for host in host_details['body']['resources']:
            print(json.dumps(host, indent=4))
    
    except Exception as e:
        print(f"An error occurred: {e}")


list_host_group_members(GROUP_ID)
