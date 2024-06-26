import os
import yaml
import json
import sys
from falconpy import Hosts, HostGroup, APIError
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


# Function to test the connection to the CrowdStrike API
def test_crowdstrike_connection(client_id, client_secret):
    try:
        falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
        response = falcon_hosts.query_devices_by_filter(limit=1)
        if response["status_code"] == 200:
            print(Fore.BLUE + "Successfully connected to the CrowdStrike API. \n Groups found in your Crowdstrike "
                              "environment: \n --------------------------------------------------" + Style.RESET_ALL)
        elif response["status_code"] == 401:
            print(Fore.RED + "Unauthorized: Please check your API credentials in the .yaml file." + Style.RESET_ALL)
            sys.exit(1)
        else:
            print(Fore.RED + f"Failed to connect to the CrowdStrike API. Status code: {response['status_code']}" +
                  Style.RESET_ALL)
            sys.exit(1)
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


# Function to un-contain a host by its ID
def uncontain_host_by_id(falcon_hosts, host_id):
    try:
        response = falcon_hosts.perform_action(action_name="lift_containment", ids=[host_id])
        return response
    except APIError as e:
        print(Fore.RED + f"APIError un-containing host ID {host_id}: {e.message}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error un-containing host ID {host_id}: {e}" + Style.RESET_ALL)
        return None


# Function to get host groups
def get_host_groups(client_id, client_secret):
    falcon = HostGroup(client_id=client_id, client_secret=client_secret)
    response = falcon.query_combined_host_groups()
    if response["status_code"] == 200:
        groups = response["body"]["resources"]
        for group in groups:
            print(f"ID: {group['id']}, Name: {group['name']}")
        return groups
    else:
        print(f"Error: {response['body']['errors'][0]['message']}")
        return []


# Function to get group members
def get_group_members(client_id, client_secret, group_id):
    falcon = HostGroup(client_id=client_id, client_secret=client_secret)
    response = falcon.query_combined_group_members(id=group_id, limit=5000)
    if response['status_code'] == 200:
        members = response["body"]["resources"]
        print("                                                                                                   ")
        print("-------------------------------------------------------------------------------------------------------------")
        print("Members found in your group:")
        for member in members:
            print(f"Host ID: {member['device_id']}, Hostname: {member['hostname']}")
        return [member['device_id'] for member in members]
    else:
        print(f"Error: {response['body']['errors'][0]['message']}")
        return []


# Function to contain hosts
def contain_hosts(hosts, client_id, client_secret):
    falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
    successfully_contained_hosts = []
    pending_contained_hosts = []
    failed_to_contain_hosts = []

    for host_id in hosts:
        containment_response = contain_host_by_id(falcon_hosts, host_id)
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


# Function to lift containment for hosts
def lift_containment(hosts, client_id, client_secret):
    falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
    successfully_uncontained_hosts = []
    pending_uncontained_hosts = []
    failed_to_uncontain_hosts = []

    for host_id in hosts:
        uncontainment_response = uncontain_host_by_id(falcon_hosts, host_id)
        if uncontainment_response:
            if uncontainment_response["status_code"] == 200 and not uncontainment_response["body"].get("errors"):
                successfully_uncontained_hosts.append(host_id)
                print(Fore.BLUE + f"Successfully un-contained {host_id}" + Style.RESET_ALL)
            elif uncontainment_response["status_code"] == 202 and not uncontainment_response["body"].get("errors"):
                pending_uncontained_hosts.append(host_id)
            else:
                failed_to_uncontain_hosts.append(host_id)
                print(Fore.RED + f"Failed to un-contain {host_id}" + Style.RESET_ALL)
        else:
            failed_to_uncontain_hosts.append(host_id)
            print(Fore.RED + f"Failed to un-contain {host_id}: No response from un-containment request" + Style.RESET_ALL)

    print_summary(successfully_uncontained_hosts, pending_uncontained_hosts, failed_to_uncontain_hosts)


# Function to print summary
def print_summary(successfully_contained_hosts, pending_contained_hosts, failed_to_contain_hosts):
    print("\n============================================================================================================")
    print(Fore.BLUE + "Successfully contained hosts:" + Style.RESET_ALL)
    for host in successfully_contained_hosts:
        print(Fore.BLUE + f"- {host}" + Style.RESET_ALL)

    print(Fore.YELLOW + "\nPending containment hosts:" + Style.RESET_ALL)
    for host in pending_contained_hosts:
        print(Fore.YELLOW + f"- {host}" + Style.RESET_ALL)

    print(Fore.RED + "\nHosts not contained:" + Style.RESET_ALL)
    for host in failed_to_contain_hosts:
        print(Fore.RED + f"- {host}" + Style.RESET_ALL)


# Function to check containment status
def containment_status(hosts, client_id, client_secret):
    falcon = Hosts(client_id=client_id, client_secret=client_secret)
    for host in hosts:
        result = falcon.get_device_details(ids=host)
        if result["status_code"] == 200:
            state = result["body"]["resources"][0]["status"]
            hostname = result["body"]["resources"][0]["hostname"]
            print(f"Hostname: {hostname}, ID: {host} ==> Status: {state}")
        else:
            print(result["body"]["errors"])


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
    selected_group_id = input("--------------------------------------------------------------------------------------\n"
                              "---Enter your Group ID: ")

    # Retrieve and display group members
    members = get_group_members(client_id, client_secret, selected_group_id)
    if not members:
        print("No members found in the selected group.")
        return

    # Contain hosts
    # contain_hosts(members, client_id, client_secret)

    while True:
        # Option to check containment status or lift containment
        action = input("----------------------------------------------------------------------------"
                       "------------------------\n Do you want to contain the hosts, check status, lift containment, or none? (contain/status/lift/none): ").lower()
        if action == "status":
            containment_status(members, client_id, client_secret)
        elif action == "contain":
            contain_hosts(members, client_id, client_secret)
        elif action == "lift":
            lift_containment(members, client_id, client_secret)
        elif action == "none":
            print("No further action taken.")
            # print("To check the containment status of provided hosts, please use 'ContainmentStatus.py' in 'Contain_Host' folder. \n Refer to the README for further
            # instructions.")
            break
        else:
            print("Invalid input. Please enter 'status', 'lift', or 'none'.")


if __name__ == "__main__":
    main()
