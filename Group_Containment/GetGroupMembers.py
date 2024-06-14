import os
import yaml
import sys
from falconpy import HostGroup

# Constants
CONFIG_FILE = 'config.yaml'
GROUP_ID = 'ac71d7e8c876456eb10424ca96f2049d'  # Replace with your actual group ID

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
falcon = HostGroup(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Function to list and print the names of the members of a host group
def list_host_group_members(group_id):
    try:
        response = falcon.query_combined_group_members(id=group_id, limit=5000)
        if response['status_code'] != 200:
            print(f"Error fetching group members: {response.get('errors', 'Unknown error')}")
            return
        
        # Extract and print host names
        members = response['body']['resources']
        if not members:
            print("No hosts found in the group.")
            return
        
        for member in members:
            print(member.get('hostname', 'Unknown hostname'))
    
    except Exception as e:
        print(f"An error occurred: {e}")

# List the members of the specified host group
list_host_group_members(GROUP_ID)
