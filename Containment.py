import os
import yaml
import json
from falconpy import Hosts, RealTimeResponse, APIError

# Constants
CONFIG_FILE = 'config.yaml'

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

# Function to read hostnames from a text file
def read_hostnames(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return []
    try:
        with open(file_path, 'r') as file:
            hostnames = [line.strip() for line in file.readlines()]
        return hostnames
    except Exception as e:
        print(f"Error reading '{file_path}': {e}")
        return []

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
        return

    # Connect to the CrowdStrike API
    try:
        falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
        # Perform a simple request to verify the connection
        response = falcon_hosts.query_devices_by_filter(limit=1)
        if response["status_code"] == 200:
            print("Successfully connected to the CrowdStrike API.")
            # Debug: Print the response from the API
            print(f"API Response: {json.dumps(response, indent=4)}")
        elif response["status_code"] == 401:
            print("Unauthorized: Please check your API credentials.")
            # Debug: Print more details for troubleshooting
            print(f"Response details: {json.dumps(response, indent=4)}")
        else:
            print(f"Failed to connect to the CrowdStrike API. Status code: {response['status_code']}")
            # Debug: Print more details for troubleshooting
            print(f"Response details: {json.dumps(response, indent=4)}")
    except APIError as e:
        print(f"APIError during authentication: {e.message}")
    except Exception as e:
        print(f"Error during API connection: {e}")

# Function to contain a host by its ID
def contain_host_by_id(falcon_hosts, host_id):
    try:
        response = falcon_hosts.perform_action(action_name="contain", ids=[host_id])
        return response
    except APIError as e:
        print(f"APIError containing host ID {host_id}: {e.message}")
    except Exception as e:
        print(f"Error containing host ID {host_id}: {e}")
        return None

# Load the configuration
config = load_config(CONFIG_FILE)

# Test the connection to the CrowdStrike API
test_crowdstrike_connection(config)

# Initialize success and failure lists
successfully_contained_hosts = []
pending_contained_hosts = []
failed_to_contain_hosts = []

# If the configuration is loaded and contains the file path, read the hostnames
if config and 'file_path' in config:
    hostnames = read_hostnames(config['file_path'])
    if hostnames:
        print(f"Read hostnames: {hostnames}")

        # Extract API credentials
        client_id = config['api']['client_id']
        client_secret = config['api']['client_secret']

        # Connect to the CrowdStrike API for containment
        try:
            falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
        except APIError as e:
            print(f"APIError during authentication: {e.message}")
        except Exception as e:
            print(f"Error during API connection: {e}")

        # Process each hostname
        for hostname in hostnames:
            try:
                # Query the API for host information based on the hostname
                response = falcon_hosts.query_devices_by_filter(filter=f"hostname:'{hostname}'")
                # Check if the response contains host details
                if response["status_code"] == 200 and "resources" in response["body"] and response["body"]["resources"]:
                    host_id = response["body"]["resources"][0]  # Get the host ID from the response
                    # Pretty print the host details
                    print(f"Host details for {hostname} ({host_id}): {json.dumps(response, indent=4)}")
                    # Contain the host using its ID
                    containment_response = contain_host_by_id(falcon_hosts, host_id)
                    # Check the containment response
                    if containment_response:
                        if containment_response["status_code"] == 200 and not containment_response["body"].get("errors"):
                            successfully_contained_hosts.append(hostname)
                            print(f"Successfully contained {hostname} ({host_id})")
                        elif containment_response["status_code"] == 202 and not containment_response["body"].get("errors"):
                            pending_contained_hosts.append(hostname)
                            print(f"Containment for {hostname} ({host_id}) is pending: {json.dumps(containment_response, indent=4)}")
                        else:
                            failed_to_contain_hosts.append(hostname)
                            print(f"Failed to contain {hostname} ({host_id}): {json.dumps(containment_response, indent=4)}")
                    else:
                        failed_to_contain_hosts.append(hostname)
                        print(f"Failed to contain {hostname} ({host_id}): No response from containment request")
                else:
                    print(f"No host found for hostname: {hostname}")
                    failed_to_contain_hosts.append(hostname)
            except APIError as e:
                print(f"APIError querying host {hostname}: {e.message}")
                failed_to_contain_hosts.append(hostname)
            except Exception as e:
                print(f"Error querying host {hostname}: {e}")
                failed_to_contain_hosts.append(hostname)
    else:
        print("No hostnames found in the specified file.")
else:
    print("File path for hostnames not specified in the configuration file.")

# Print summary
print("\nSummary:")
print("Successfully contained hosts:")
for host in successfully_contained_hosts:
    print(f"- {host}")

print("\nPending containment hosts:")
for host in pending_contained_hosts:
    print(f"- {host}")

print("\nFailed to contain hosts:")
for host in failed_to_contain_hosts:
    print(f"- {host}")
