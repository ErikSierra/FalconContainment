import os
import yaml
from falconpy import Hosts, APIError

# Constants
CONFIG_FILE = 'config.yaml'

# Function to test the connection to the CrowdStrike API
def test_crowdstrike_connection():
    # Check if the configuration file exists
    if not os.path.isfile(CONFIG_FILE):
        print(f"Error: Configuration file '{CONFIG_FILE}' not found.")
        return
    else:
        print(f"Configuration file '{CONFIG_FILE}' found! Checking connection...")

    # Load the API credentials from the configuration file
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