import os
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


# Function to read hostnames from a text file
def read_hostnames(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    try:
        with open(file_path, 'r') as file:
            hostnames = [line.strip() for line in file.readlines()]
        return hostnames
    except Exception as e:
        print(f"Error reading '{file_path}': {e}")
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


# Function to contain a host by its ID
def contain_host_by_id(falcon_hosts, host_id):
    try:
        response = falcon_hosts.perform_action(action_name="contain", ids=[host_id])
        return response
    except APIError as e:
        print(Fore.RED + f"APIError containing host ID {host_id}: {e.message}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error containing host ID {host_id}: {e}" + Style.RESET_ALL)
        return None


# Load the configuration
config = load_config(CONFIG_FILE)

# Test the connection to the CrowdStrike API
test_crowdstrike_connection(config)

# Initialize success and failure lists
successfully_contained_hosts = []
pending_contained_hosts = []
failed_to_contain_hosts = []

# If the configuration is loaded and contains the file path, read the hostnames (lots of conditionals)
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
            print(Fore.RED + f"APIError during authentication: {e.message}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error during API connection: {e}" + Style.RESET_ALL)

        # Process each hostname
        for hostname in hostnames:
            try:
                # Query the API for host information based on the hostname
                response = falcon_hosts.query_devices_by_filter(filter=f"hostname:'{hostname}'")
                # Check if the response contains host details
                if response["status_code"] == 200 and "resources" in response["body"] and response["body"]["resources"]:
                    host_id = response["body"]["resources"][0]  # Get the host ID from the response
                    # Pretty print the host details
                    # print(f"Host details for {hostname} ({host_id}): {json.dumps(response, indent=4)}")
                    # Contain the host using its ID
                    containment_response = contain_host_by_id(falcon_hosts, host_id)
                    # Check the containment response
                    if containment_response:
                        if containment_response["status_code"] == 200 and not containment_response["body"].get(
                                "errors"):
                            successfully_contained_hosts.append(hostname)
                            print(Fore.BLUE + "Successfully contained {hostname} ({host_id})" + Style.RESET_ALL)
                        elif containment_response["status_code"] == 202 and not containment_response["body"].get(
                                "errors"):
                            pending_contained_hosts.append(hostname)
                            # print(Fore.YELLOW + "Containment for {hostname} ({host_id}) is pending: {json.dumps"
                            #                     "(containment_response, indent=4)}" + Style.RESET_ALL)
                        else:
                            failed_to_contain_hosts.append(hostname)
                            print(Fore.RED + f"Failed to contain {hostname} ({host_id}): {json.dumps(containment_response, indent=4)}" + Style.RESET_ALL)
                    else:
                        failed_to_contain_hosts.append(hostname)
                        print(Fore.RED + f"Failed to contain {hostname} ({host_id}): No response from containment "
                                         f"request" + Style.RESET_ALL)
                else:
                    print(Fore.RED + f"No host found for hostname: {hostname}" + Style.RESET_ALL)
                    failed_to_contain_hosts.append(hostname)
            except APIError as e:
                print(Fore.RED + f"APIError querying host {hostname}: {e.message}" + Style.RESET_ALL)
                failed_to_contain_hosts.append(hostname)
            except Exception as e:
                print(Fore.RED + f"Error querying host {hostname}: {e}" + Style.RESET_ALL)
                failed_to_contain_hosts.append(hostname)
    else:
        print(Fore.RED + "No hostnames found in the specified file.")
else:
    print("File path for hostnames not specified in the configuration file.")

# Print summary
print("\n============================================================================================================"
      "=============================")
print(Fore.BLUE + "Successfully contained hosts:" + Style.RESET_ALL)
for host in successfully_contained_hosts:
    print(Fore.BLUE + "- {host}")

print(Fore.YELLOW + "\nPending containment hosts:" + Style.RESET_ALL)
for host in pending_contained_hosts:
    print(Fore.YELLOW + f"- {host}")

print(Fore.RED + "\nFailed to contain hosts:" + Style.RESET_ALL)
for host in failed_to_contain_hosts:
    print(Fore.RED + f"- {host}")

status = input("===============================================================================\n"
               "Do you want to re-check the status of containment for these hosts? (Y/N) ")
if status.lower() == 'n':
    print("Exiting the script...")
    exit()
elif status.lower() == 'y':
    print("Running ContainmentStatus.py and checking status of hosts.")
    venv_python = sys.executable
    containment_script = "ContainmentStatus.py"
    subprocess.call([venv_python, containment_script])
else:
    print("Invalid input. Please enter Y or N.")
