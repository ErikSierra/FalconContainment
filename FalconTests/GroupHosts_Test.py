import yaml
from falconpy import HostGroup, Hosts, APIHarness

# Constants
CONFIG_FILE = 'config.yaml'
GROUP_ID = 'your_group_id'  # Replace with your actual group ID

# Function to load configuration
def load_config(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: Configuration file '{file_path}' not found.")
        return None

    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
            return config
    except yaml.YAMLError as e:
        print(f"Error reading configuration file: {e}")
        return None

# Load the configuration
config = load_config(CONFIG_FILE)
if not config:
    sys.exit(1)

CLIENT_ID = config['api']['client_id']
CLIENT_SECRET = config['api']['client_secret']

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