"""
Note:
    This script is for testing purposes to attempt connection to API in Crowdstrike Falcon
This script does not perform any official API containment within Crowdstrike Falcon or related resources.
Use 'Containment.py' for Crowdstrike API containment process/tests
"""

import os
from falconpy import Hosts, APIError

'''
In cmd:
set CROWDSTRIKE_CLIENT_ID=your_client_id_here
set CROWDSTRIKE_CLIENT_SECRET=your_client_secret_here
python APIconnectionTest.py
test
'''


# Function to test the connection to the CrowdStrike API
def test_crowdstrike_connection():
    # API credentials (get these from environment variables for security)
    client_id = os.getenv('CROWDSTRIKE_CLIENT_ID')
    client_secret = os.getenv('CROWDSTRIKE_CLIENT_SECRET')

    # Check if API credentials are available
    if not client_id or not client_secret:
        print("Error: CrowdStrike API credentials are not set in the environment variables.")
        return

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
