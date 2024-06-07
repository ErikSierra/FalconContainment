import os
import falconpy
import yaml
import json
import sys
from falconpy import Hosts, RealTimeResponse, APIError
from colorama import init, Fore, Back, Style
import subprocess
import sys


init()

# Constants
CONFIG_FILE = 'config.yaml'


# Function to load configuration
def load_config(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: Configuration file '{file_path}' not found.")
        sys.exit(1)

    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
            return config
    except yaml.YAMLError as e:
        print(f"Error reading configuration file: {e}")
        sys.exit(1)


# Function to test the connection to the CrowdStrike API
def test_crowdstrike_connection(config):
    if not config:
        return

    try:
        # API credentials
        client_id = config['api']['client_id']
        client_secret = config['api']['client_secret']
    except KeyError as e:
        print(f"Missing API credential in configuration file: {e}")
        sys.exit(1)

    # Connect to the CrowdStrike API
    try:
        falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
        # Perform a simple request to verify the connection
        response = falcon_hosts.query_devices_by_filter(limit=1)
        if response["status_code"] == 200:
            print(Fore.BLUE + "Successfully connected to the CrowdStrike API." + Style.RESET_ALL)
            # Debug: Print the response from the API
            # print(f"API Response: {json.dumps(response, indent=4)}")
        elif response["status_code"] == 401:
            print(Fore.RED + "Unauthorized: Please check your API credentials in the .yaml file." + Style.RESET_ALL)
            sys.exit(1)
            # Debug: Print more details for troubleshooting
            # print(Fore.RED + f"Response details: {json.dumps(response, indent=4)}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Failed to connect to the CrowdStrike API. Status code: {response['status_code']}" +
                  Style.RESET_ALL)
            sys.exit(1)
            # Debug: Print more details for troubleshooting
            # print(f"Response details: {json.dumps(response, indent=4)}")
    except APIError as e:
        print(Fore.RED + f"APIError during authentication: {e.message}" + Style.RESET_ALL)
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"Error during API connection: {e}" + Style.RESET_ALL)
        sys.exit(1)


# Define the ID of the Host Group to be contained
host_group_id = "ac71d7e8c876456eb10424ca96f2049d"

# Define the duration of the containment in seconds
containment_duration = 3600

# Initiate containment for the Host Group
def contain_host_by_id(falcon_hosts, host_id):
    try:
        response = falcon_hosts.perform_action(action_name="contain", ids=[host_id])
        return response
    except APIError as e:
        print(Fore.RED + f"APIError containing host ID {host_id}: {e.message}" + Style.RESET_ALL)
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"Error containing host ID {host_id}: {e}" + Style.RESET_ALL)
        sys.exit(1)


# Load configuration file
config = load_config(CONFIG_FILE)

# Test connection to CrowdStrike API
test_crowdstrike_connection(config)

# Connect to the CrowdStrike Hosts API
falcon_hosts = Hosts(access_token=config['api']['access_token'])

# Initiate containment for all Hosts in the Host Group
try:
    # Query the Host Group to get a list of Host IDs
    print("Querying the Host Group for Host IDs...")
    query = falcon_hosts.query_devices(filter=f"falcon_host_group_id:'{host_group_id}'")
    if query["status_code"] != 200:
        print(Fore.RED + f"Error querying Hosts: {query['status_code']} {query['body']}" + Style.RESET_ALL)
        sys.exit(1)
    hosts = [device['id'] for device in query['body']['resources']]
    print(Fore.BLUE + f"Found {len(hosts)} Hosts in the Host Group." + Style.RESET_ALL)

    # Initiate containment for each Host
    for host_id in hosts:
        print(f"Initiating containment for Host ID: {host_id}")
        response = contain_host_by_id(falcon_hosts, host_id)
        if response["status_code"] == 200:
            print(Fore.GREEN + f"Containment successfully initiated for Host ID: {host_id}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Failed to initiate containment for Host ID: {host_id}. Status code: {response['status_code']}" + Style.RESET_ALL)

except APIError as e:
    print(Fore.RED + f"APIError when querying Host Group: {e.message}" + Style.RESET_ALL)
    sys.exit(1)
except Exception as e:
    print(Fore.RED + f"Error when querying Host Group: {e}" + Style.RESET_ALL)
    sys.exit(1)