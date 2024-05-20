import os
import yaml
from falconpy import Hosts, RealTimeResponse, APIError


# Function to contain a host by its ID
def contain_host_by_id(falcon_rtr, host_id):
    try:
        response = falcon_rtr.contain_host(device_id=host_id)
        return response
    except APIError as e:
        print(f"APIError containing host ID {host_id}: {e.message}")
    except Exception as e:
        print(f"Error containing host ID {host_id}: {e}")


# Function to read the configuration from a YAML file
def read_config(filename):
    try:
        with open(filename, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return {}
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return {}


# Connect to the CrowdStrike API using the configuration file
config = read_config("config.yaml")
client_id = config.get('api', {}).get('client_id', None)
client_secret = config.get('api', {}).get('client_secret', None)
file_path = config.get('file_path', None)

if not client_id or not client_secret:
    exit("Error: CrowdStrike API credentials are missing from config file.")

if not file_path:
    exit("Error: File path is missing from config file.")

try:
    falcon_hosts = Hosts(client_id=client_secret, client_secret=client_secret)
    falcon_rtr = RealTimeResponse(client_id=client_id, client_secret=client_secret)
except APIError as e:
    exit(f"APIError during authentication: {e.message}")
except Exception as e:
    exit(f"Error during API connection: {e}")

# Read hostnames from the file
try:
    with open(file_path, 'r') as file:
        hostnames = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    exit(f"Error: The file {file_path} was not found.")
except Exception as e:
    exit(f"Error reading {file_path}: {e}")

if not hostnames:
    exit("Exiting due to missing or empty hostname file.")

# Look up each hostname using the CrowdStrike API
for hostname in hostnames:
    try:
        # Query the API for host information based on the hostname
        response = falcon_hosts.query_devices_by_filter(filter=f"hostname:'{hostname}'")
        # Check if the response contains host details
        if response["status_code"] == 200 and "resources" in response["body"] and response["body"]["resources"]:
            host_id = response["body"]["resources"][0]  # Get the host ID from the response
            # Contain the host using its ID
            containment_response = contain_host_by_id(falcon_rtr, host_id)
            # Print the containment response
            if containment_response:
                print(f"Containment response for {hostname} ({host_id}): {containment_response}")
        else:
            print(f"No host found for hostname: {hostname}")
    except APIError as e:
        print(f"APIError querying host {hostname}: {e.message}")
    except Exception as e:
        print(f"Error querying host {hostname}: {e}")
