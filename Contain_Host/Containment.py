import os
import yaml
import json
import sys
from falconpy import Hosts, RealTimeResponse, APIError
from colorama import init, Fore, Back, Style
import subprocess
import sys
from datetime import datetime
import time

def log_containment_action(hostname, host_id, status):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - Hostname: {hostname}, Host ID: {host_id}, Status: {status}\n"
    with open("containment_log.txt", "a") as log_file:
        log_file.write(log_message)

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

# Initialize success and failure lists
successfully_contained_hosts = []
pending_contained_hosts = []
failed_to_contain_hosts = []

# If the configuration is loaded and contains the file path, read the hostnames (lots of conditionals)
if config and 'file_path' in config:
    hostids = read_hostnames(config['file_path'])
    if hostids:
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

        # Inside your loop where you process each hostname
        for hostid in hostids:
            try:
                # Query the API for host information based on the hostname
                response = falcon_hosts.query_devices_by_filter(filter=f"hostname:'{hostid}'")
                # Check if the response contains host details
                if response["status_code"] == 200 and "resources" in response["body"] and response["body"]["resources"]:
                    host_id = response["body"]["resources"][0]  # Get the host ID from the response
                    # Contain the host using its ID
                    contain_host_by_id(falcon_hosts, host_id)
                else:
                    print(Fore.RED + f"No host found for hostname: {hostid}" + Style.RESET_ALL)
            except APIError as e:
                print(Fore.RED + f"APIError querying host {hostid}: {e.message}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error querying host {hostid}: {e}" + Style.RESET_ALL)

        time.sleep(60)

        for hostid in hostids:
            # Query the API for host information based on the hostname
            response = falcon_hosts.query_devices_by_filter(filter=f"hostname:'{hostid}'")
            host_id = response["body"]["resources"][0] 
            result = falcon_hosts.get_device_details(ids=host_id)

            if result["status_code"] == 200:
                status = result["body"]["resources"][0]["status"]
                hostname = result["body"]["resources"][0]["hostname"]
                if status == "contained":
                    successfully_contained_hosts.append([hostname, host_id])
                elif status == "normal":
                    failed_to_contain_hosts.append([hostname, host_id])
                else:
                    pending_contained_hosts.append([hostname, host_id])
            else:
                print(result["body"]["errors"])

        print("SuccessFully Contained: \n")
        for i in range(len(successfully_contained_hosts)):
            name, id = successfully_contained_hosts[i]
            print("Host name: ", name, " Host id: ", id)
            log_containment_action(name, id, "contained")
    
        print("Pending containment: \n")
        for i in range(len(pending_contained_hosts)):
            name, id = pending_contained_hosts[i]
            print("Host name: ", name, " Host id: ", id)
            log_containment_action(name, id, "pending")

        print("Failed containment: \n")
        for i in range(len(failed_to_contain_hosts)):
            name, id = failed_to_contain_hosts[i]
            print("Host name: ", name, " Host id: ", id)
            log_containment_action(name, id, "normal")

    else:
        print(Fore.RED + "No hostnames found in the specified file.")
else:
    print("File path for hostnames not specified in the configuration file.")







# # Print summary
# print("\n============================================================================================================"
#       "=============================")
# print(Fore.BLUE + "Successfully contained hosts:" + Style.RESET_ALL)
# for host in successfully_contained_hosts:
#     print(Fore.BLUE + f"- {host}" + Style.RESET_ALL)

# print(Fore.YELLOW + "\nPending containment hosts:" + Style.RESET_ALL)
# for host in pending_contained_hosts:
#     print(Fore.YELLOW + f"- {host}" + Style.RESET_ALL)

# print(Fore.RED + "\nFailed to contain hosts:" + Style.RESET_ALL)
# for host in failed_to_contain_hosts:
#     print(Fore.RED + f"- {host}" + Style.RESET_ALL)

# status = input("===============================================================================\n"
#                "Do you want to re-check the status of containment for these hosts? (Y/N) ")
# if status.lower() == 'n':
#     print("Exiting the script...")
#     exit()
# elif status.lower() == 'y':
#     print("Running ContainmentStatus.py and checking status of hosts.")
#     venv_python = sys.executable
#     containment_script = "ContainmentStatus.py"
#     subprocess.call([venv_python, containment_script])
# else:
#     print("Invalid input. Please enter Y or N.")
