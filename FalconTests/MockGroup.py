import os
import yaml
import json
import sys
from colorama import init, Fore, Style

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

# Function to simulate testing the connection to the CrowdStrike API
def test_crowdstrike_connection(client_id, client_secret):
    print(Fore.BLUE + "Successfully connected to the CrowdStrike API (simulated)." + Style.RESET_ALL)

# Function to simulate containing a host by its ID
def contain_host_by_id(falcon_hosts, host_id):
    if host_id == "host1":
        return {"status_code": 200, "body": {"errors": []}}
    elif host_id == "host2":
        return {"status_code": 202, "body": {"errors": []}}
    else:
        return {"status_code": 400, "body": {"errors": ["Simulated error"]}}

# Function to simulate un-containing a host by its ID
def uncontain_host_by_id(falcon_hosts, host_id):
    if host_id == "host1":
        return {"status_code": 200, "body": {"errors": []}}
    elif host_id == "host2":
        return {"status_code": 202, "body": {"errors": []}}
    else:
        return {"status_code": 400, "body": {"errors": ["Simulated error"]}}

# Function to simulate getting host groups
def get_host_groups(client_id, client_secret):
    groups = [
        {"id": "group1", "name": "Test Group 1"},
        {"id": "group2", "name": "Test Group 2"}
    ]
    for group in groups:
        print(f"ID: {group['id']}, Name: {group['name']}")
    return groups

# Function to simulate getting group members
def get_group_members(client_id, client_secret, group_id):
    members = [
        {"device_id": "host1", "hostname": "Host 1"},
        {"device_id": "host2", "hostname": "Host 2"},
        {"device_id": "host3", "hostname": "Host 3"}
    ]
    for member in members:
        print(f"Host ID: {member['device_id']}, Hostname: {member['hostname']}")
    return [member['device_id'] for member in members]

# Function to simulate containing hosts
def contain_hosts(hosts, client_id, client_secret):
    successfully_contained_hosts = []
    pending_contained_hosts = []
    failed_to_contain_hosts = []

    for host_id in hosts:
        containment_response = contain_host_by_id(None, host_id)
        if containment_response:
            if containment_response["status_code"] == 200 and not containment_response["body"].get("errors"):
                successfully_contained_hosts.append(host_id)
                print(Fore.BLUE + f"Successfully contained {host_id}" + Style.RESET_ALL)
            elif containment_response["status_code"] == 202 and not containment_response["body"].get("errors"):
                pending_contained_hosts.append(host_id)
            else:
                failed_to_contain_hosts.append(host_id)
                print(Fore.RED + f"Failed to contain {host_id}: {json.dumps(containment_response, indent=4)}" + Style.RESET_ALL)
        else:
            failed_to_contain_hosts.append(host_id)
            print(Fore.RED + f"Failed to contain {host_id}: No response from containment request" + Style.RESET_ALL)
    
    print_summary(successfully_contained_hosts, pending_contained_hosts, failed_to_contain_hosts)

# Function to simulate lifting containment for hosts
def lift_containment(hosts, client_id, client_secret):
    successfully_uncontained_hosts = []
    pending_uncontained_hosts = []
    failed_to_uncontain_hosts = []

    for host_id in hosts:
        uncontainment_response = uncontain_host_by_id(None, host_id)
        if uncontainment_response:
            if uncontainment_response["status_code"] == 200 and not uncontainment_response["body"].get("errors"):
                successfully_uncontained_hosts.append(host_id)
                print(Fore.BLUE + f"Successfully un-contained {host_id}" + Style.RESET_ALL)
            elif uncontainment_response["status_code"] == 202 and not uncontainment_response["body"].get("errors"):
                pending_uncontained_hosts.append(host_id)
            else:
                failed_to_uncontain_hosts.append(host_id)
                print(Fore.RED + f"Failed to un-contain {host_id}: {json.dumps(uncontainment_response, indent=4)}" + Style.RESET_ALL)
        else:
            failed_to_uncontain_hosts.append(host_id)
            print(Fore.RED + f"Failed to un-contain {host_id}: No response from un-containment request" + Style.RESET_ALL)
    
    print_summary(successfully_uncontained_hosts, pending_uncontained_hosts, failed_to_uncontain_hosts)

# Function to simulate printing summary
def print_summary(successfully_contained_hosts, pending_contained_hosts, failed_to_contain_hosts):
    print("\n============================================================================================================")
    print(Fore.BLUE + "Successfully contained hosts:" + Style.RESET_ALL)
    for host in successfully_contained_hosts:
        print(Fore.BLUE + f"- {host}" + Style.RESET_ALL)

    print(Fore.YELLOW + "\nPending containment hosts:" + Style.RESET_ALL)
    for host in pending_contained_hosts:
        print(Fore.YELLOW + f"- {host}" + Style.RESET_ALL)

    print(Fore.RED + "\nFailed to contain hosts:" + Style.RESET_ALL)
    for host in failed_to_contain_hosts:
        print(Fore.RED + f"- {host}" + Style.RESET_ALL)

# Function to simulate checking containment status
def containment_status(hosts, client_id, client_secret):
    for host in hosts:
        if host == "host1":
            state = "contained"
        elif host == "host2":
            state = "containment_pending"
        else:
            state = "failed"
        print(f"Hostname: {host}, ID: {host} ==> Status: {state}")

def main():
    # Load the configuration
    config = load_config(CONFIG_FILE)
    if not config:
        return

    client_id = config['api']['client_id']
    client_secret = config['api']['client_secret']

    # Test the connection to the CrowdStrike API
    test_crowdstrike_connection(client_id, client_secret)

    # Retrieve and display host groups
    groups = get_host_groups(client_id, client_secret)
    if not groups:
        return

    # User selects a group ID
    selected_group_id = input("Enter the Group ID to contain: ")

    # Retrieve and display group members
    members = get_group_members(client_id, client_secret, selected_group_id)
    if not members:
        print("No members found in the selected group.")
        return

    # Contain hosts
    contain_hosts(members, client_id, client_secret)

    # Option to check containment status or lift containment
    action = input("Do you want to check containment status or lift containment? (status/lift/none): ").lower()
    if action == "status":
        containment_status(members, client_id, client_secret)
    elif action == "lift":
        lift_containment(members, client_id, client_secret)
    else:
        print("No further action taken.")

if __name__ == "__main__":
    main()
