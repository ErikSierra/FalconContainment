import os
import falconpy
import yaml
import json
import sys
from falconpy import Hosts, RealTimeResponse, APIError
from colorama import init, Fore, Back, Style
import subprocess
import sys

from FalconTests.APIconnectionTest import falcon_hosts

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
    except Exception as e:
        print(Fore.RED + f"Error containing host ID {host_id}: {e}" + Style.RESET_ALL)
        return None


'''    data={
        "action": "contain",
        "ids": [
            host_group_id
        ],
        "parameters": {
            "duration": containment_duration
        }
    }
)'''

# Check for success/failure of containment request
if response["status_code"] == 201:
    print("Containment request successful.")
else:
    print(f"Containment request failed with error code - {response['status_code']}.")