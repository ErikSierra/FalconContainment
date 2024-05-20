"""
Note:
    This script is for testing purposes to attempt connection to API in Crowdstrike Falcon
This script does not perform any official API containment within Crowdstrike Falcon or related resources.
Use 'Containment.py' for Crowdstrike API containment process/tests
"""

import os
import yaml
from falconpy import Hosts, APIError

'''
In cmd:
python APIconnectionTest.py
'''

CONFIG_FILE = 'config.yaml'


# Function to test the connection to the CrowdStrike API
def test_crowdstrike_connection():
    # Load the API credentials and file path from the configuration file
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # API credentials
    client_id = config['api']['client_id']
    client_secret = config['api']['client_secret']

    # Connect to the CrowdStrike API
    try:
        falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
        # Perform a simple request to verify the connection, e.g., get a list of devices
        response = falcon_hosts.query_devices_by_filter(limit=1)
        if response["status_code"] == 200:
            print("Successfully connected to the CrowdStrike API.")
        else:
            print(f"Failed to connect to the CrowdStrike API. Status code: {response['status_code']}")
    except APIError as e:
        print(f"APIError during authentication: {e.message}")
    except Exception as e:
        print(f"Error during API connection: {e}")


# Run the test
test_crowdstrike_connection()