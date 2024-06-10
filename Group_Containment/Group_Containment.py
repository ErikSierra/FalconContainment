import os
import yaml
import sys
from falconpy import HostGroup, Hosts

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

# Function to list the members of a host group
def list_host_group_members(group_id):
    try:
        # Create an instance of HostGroup
        host_group = HostGroup(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        
        # Get the list of host IDs in the group
        response = host_group.query_group_members(limit=5000, id=group_id)
        print(f"Debug: Full response from query_group_members: {response}")
        if response['status_code'] != 200:
            print(f"Error fetching group members: {response.get('errors', 'Unknown error')}")
            return []
        
        # Extract host IDs
        host_ids = response['body']['resources']
        if not host_ids:
            print("No hosts found in the group.")
            return []
        
        return host_ids
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Function to contain a host by its ID
def contain_host_by_id(host_id):
    try:
        hosts = Hosts(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        response = hosts.perform_action(action_name="contain", ids=[host_id])
        if response['status_code'] == 200:
            return True
        else:
            # Print detailed error message
            error_message = response.get('body', {}).get('errors', response)
            print(f"Failed to contain host {host_id}: {error_message}")
            return False
    except Exception as e:
        print(f"An error occurred while containing host {host_id}: {e}")
        return False

# Function to process containment for each host in the group
def contain_group_hosts(group_id):
    host_ids = list_host_group_members(group_id)
    if not host_ids:
        return

    successfully_contained_hosts = []
    failed_to_contain_hosts = []

    for host_id in host_ids:
        if contain_host_by_id(host_id):
            successfully_contained_hosts.append(host_id)
        else:
            failed_to_contain_hosts.append(host_id)

    print("\nSuccessfully contained hosts:")
    for host_id in successfully_contained_hosts:
        print(f"- {host_id}")

    print("\nFailed to contain hosts:")
    for host_id in failed_to_contain_hosts:
        print(f"- {host_id}")

# Contain the members of the specified host group
contain_group_hosts(GROUP_ID)