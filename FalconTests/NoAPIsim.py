"""
Note:
    This script is for testing purposes to attempt a mock simulation of 'Containment.py'
This script does not perform any official API containment within Crowdstrike Falcon or related resources.
Use 'Containment.py' for Crowdstrike API containment.
Refer to the GitHub repository for instructions.
"""

import os
import yaml
import json
from colorama import init, Fore, Back, Style
import sys

init()
# Constants
CONFIG_FILE = 'config.yaml'


# Function to load configuration
def load_config(file_path):
    if not os.path.isfile(file_path):
        print(Fore.RED + f"Error: Configuration file '{file_path}' not found." + Style.RESET_ALL)
        sys.exit(1)
    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
            return config
    except yaml.YAMLError as e:
        print(Fore.RED + f"Error reading configuration file: {e}" + Style.RESET_ALL)
        sys.exit(1)


# Function to read hostnames from a text file
def read_hostnames(file_path):
    if not os.path.isfile(file_path):
        print(Fore.RED + f"Error: The file '{file_path}' was not found." + Style.RESET_ALL)
        sys.exit(1)
    try:
        with open(file_path, 'r') as file:
            hostnames = [line.strip() for line in file.readlines()]
        return hostnames
    except Exception as e:
        print(Fore.RED + f"Error reading '{file_path}': {e}" + Style.RESET_ALL)
        sys.exit(1)


# Test the connection to the CrowdStrike API
def test_crowdstrike_connection(config):
    if not config:
        return

    try:
        client_id = config['api']['client_id']
        client_secret = config['api']['client_secret']
    except KeyError as e:
        print(Fore.RED + f"Missing API credential in configuration file: {e}" + Style.RESET_ALL)
        sys.exit(1)

    try:
        # Simulate successful connection to CrowdStrike API
        print("Successfully connected to the CrowdStrike API.")
    except APIError as e:
        print(Fore.RED + f"APIError during authentication: {e.message}" + Style.RESET_ALL)
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"Error during API connection: {e}" + Style.RESET_ALL)
        sys.exit(1)


# Load the configuration
config = load_config(CONFIG_FILE)

# Test the connection to the CrowdStrike API
test_crowdstrike_connection(config)

rerun_check = True
while rerun_check:
    # Initialize status lists
    contained_hosts = []
    pending_hosts = []
    failed_hosts = []

    # If the configuration is loaded and contains the file path, read the hostnames
    if config and 'file_path' in config:
        hostnames = read_hostnames(config['file_path'])
        if hostnames:
            print("==================================================================================================="
                  "======================================")
            print(Fore.BLUE + "Read hostnames:" + Style.RESET_ALL)
            for hostname in hostnames:
                print(hostname)
            print("==================================================================================================="
                  "======================================")

            # Process each hostname
            for hostname in hostnames:
                try:
                    # Simulate response from CrowdStrike API
                    response = {
                        "status_code": 200,
                        "body": {
                            "resources": ["1234567890"]
                        }
                    }
                    # Check if the response contains host details
                    if response["status_code"] == 200 and "resources" in response["body"] and response["body"]["resources"]:
                        host_id = response["body"]["resources"][0]  # Get the host ID from the response
                        # Pretty print the host details
                        # print(f"Host details for {hostname} ({host_id}): {json.dumps(response, indent=4)}")
                        # Simulate successful containment status response from CrowdStrike API
                        containment_status_response = {
                            "status_code": 200,
                            "body": {
                                "resources": [
                                    {
                                        "id": "1234567890",
                                        "status": "contained"
                                    }
                                ]
                            }
                        }
                        # Debug: Print the full containment status response print(f"Containment status response for {
                        # hostname} ({host_id}): {json.dumps(containment_status_response, indent=4)}") Check the
                        # containment status response and update the status lists
                        if containment_status_response and containment_status_response['status_code'] == 200 and containment_status_response['body']['resources']:
                            containment_status = containment_status_response['body']['resources'][0].get('status', None)
                            if containment_status == "contained":
                                contained_hosts.append(hostname)
                                # print(Fore.BLUE + f"{hostname}: Contained" + Style.RESET_ALL)
                            elif containment_status == "containment_pending":
                                pending_hosts.append(hostname)
                                # print(Fore.YELLOW + f"{hostname}: Containment pending" + Style.RESET_ALL)
                            else:
                                failed_hosts.append(hostname)
                                # print(Fore.RED + f"{hostname}: Not contained" + Style.RESET_ALL)
                        else:
                            failed_hosts.append(hostname)
                            print(Fore.RED + f"{hostname}: Error getting containment status" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + f"No host found for hostname: {hostname}" + Style.RESET_ALL)
                        failed_hosts.append(hostname)
                except APIError as e:
                    print(Fore.RED + f"APIError querying host {hostname}: {e.message}" + Style.RESET_ALL)
                    failed_hosts.append(hostname)
                except Exception as e:
                    print(Fore.RED + f"Error querying host {hostname}: {e}" + Style.RESET_ALL)
                    failed_hosts.append(hostname)
        else:
            print(Fore.RED + "No hostnames found in the specified file." + Style.RESET_ALL)
    else:
        print(Fore.RED + "File path for hostnames not specified in the configuration file.")

    # Print summary
    print("==========================================================================================================="
          "==============================")
    print(Fore.BLUE + "Contained hosts:")
    for host in contained_hosts:
        print(f"{host}")

    print(Fore.YELLOW + "\nPending containment hosts:")
    for host in pending_hosts:
        print(f"{host}")

    print(Fore.RED + "\nNon-contained hosts:")
    for host in failed_hosts:
        print(f"{host}")

    # Ask user if they want to rerun the check again
    user_input = input(Fore.BLUE + "\n============================================================================================"
                       "=============================================\nDo you want to rerun the check again? (Y/N) ")
    if user_input.lower() == "n":
        rerun_check = False
        print("Exiting the script...")
    else:
        print(Fore.BLUE + "============================================================================================"
                          "============================================================================================"
                          "==========\n"
              "Rerunning the check...")