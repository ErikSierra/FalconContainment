from falconpy import HostGroup, Hosts, APIHarness

# Constants
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
GROUP_ID = 'your_group_id'  # Replace with your actual group ID

# Initialize the API harness
falcon = APIHarness(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Function to list the members of a host group
def list_host_group_members(group_id):
    try:
        # Create an instance of HostGroup
        host_group = HostGroup(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        
        # Get the list of host IDs in the group
        response = host_group.query_group_members(limit=5000, id=group_id)
        if response['status_code'] != 200:
            print(f"Error fetching group members: {response['errors']}")
            return
        
        # Extract host IDs
        host_ids = response['body']['resources']
        if not host_ids:
            print("No hosts found in the group.")
            return
        
        # Fetch details for each host
        hosts = Hosts(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        host_details = hosts.get_device_details(ids=host_ids)
        
        # Print the names of each host
        for host in host_details['body']['resources']:
            print(host.get('hostname', 'Unknown hostname'))
    
    except Exception as e:
        print(f"An error occurred: {e}")

# List the members of the specified host group
list_host_group_members(GROUP_ID)