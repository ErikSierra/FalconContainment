import json
import sys
from falconpy import Hosts, HostGroup, APIError
from colorama import init, Fore, Style
from LoadConfig import load_config # loads config.yaml
import pandas as pd
init()
from datetime import datetime
import time

def log_containment_action(hostname, host_id, action, status):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - Hostname: {hostname}, Host ID: {host_id}, Action: {action}, Status: {status}\n"
    with open("group_containment_log.txt", "a") as log_file:
        log_file.write(log_message)

# Function to test the connection to the CrowdStrike API
def test_crowdstrike_connection(client_id, client_secret):
    try:
        falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
        response = falcon_hosts.query_devices_by_filter(limit=1)
        if response["status_code"] == 200:
            print(Fore.BLUE + "Successfully connected to the CrowdStrike API \nGroups found in your Crowdstrike environment:"
                   + Style.RESET_ALL)
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
    groupsID, groupsName = list(), list()
    
    if response["status_code"] == 200:
        groups = response["body"]["resources"]
        for group in groups:
            groupsID.append(group['id'])
            groupsName.append(group['name'])
        data = {
            'Group Name' : groupsName,
            'Group Ids' : groupsID
        }
        pd.set_option('display.max_rows', None)
        df = pd.DataFrame(data) 
        print("\n", df, "\n")
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
        hostNames, hostIds = list(), list()
        for member in members:
            hostNames.append(member['device_id'])
            hostIds.append(member['hostname'])
        data = {
            'Host Name' : hostNames,
            'Host Ids' : hostIds
        }
        pd.set_option('display.max_rows', None)
        df = pd.DataFrame(data) 
        print("\n", df, "\n")
        return [member['device_id'] for member in members]
    else:
        print(f"Error: {response['body']['errors'][0]['message']}")
        return []
    

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

# Function to contain hosts
def contain_hosts(hosts, client_id, client_secret):
    falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
    successfully_contained_hosts = []
    pending_contained_hosts = []
    failed_to_contain_hosts = []

    for host_id in hosts:
        contain_host_by_id(falcon_hosts, host_id)

    time.sleep(60)

    # Check the status post-delay
    status_response = containment_status(hosts, client_id, client_secret)
    for host_id, (hostname, status) in status_response.items():
        if status.lower() == "contained":
            successfully_contained_hosts.append(host_id)
            print(Fore.BLUE + f"Successfully contained {hostname} ({host_id})" + Style.RESET_ALL)
            log_containment_action(hostname, host_id, "contain", "success")
        elif status.lower() == "pending":
            pending_contained_hosts.append(host_id)
            log_containment_action(hostname, host_id, "contain", "pending")
        else:
            failed_to_contain_hosts.append(host_id)
            print(Fore.RED + f"Failed to contain {hostname} ({host_id})" + Style.RESET_ALL)
            log_containment_action(hostname, host_id, "contain", "failed")

    print_summary(successfully_contained_hosts, pending_contained_hosts, failed_to_contain_hosts)


# Function to lift containment for hosts
def lift_containment(hosts, client_id, client_secret):
    falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
    successfully_uncontained_hosts = []
    pending_uncontained_hosts = []
    failed_to_uncontain_hosts = []

    for host_id in hosts:
        uncontain_host_by_id(falcon_hosts, host_id)

    time.sleep(60)

    # Check the status post-delay
    status_response = containment_status(hosts, client_id, client_secret)
    for host_id, (hostname, status) in status_response.items():
        if status.lower() == "contained":
            successfully_uncontained_hosts.append(host_id)
            print(Fore.BLUE + f"Successfully contained {hostname} ({host_id})" + Style.RESET_ALL)
            log_containment_action(hostname, host_id, "contain", "success")
        elif status.lower() == "pending":
            pending_uncontained_hosts.append(host_id)
            log_containment_action(hostname, host_id, "contain", "pending")
        else:
            failed_to_uncontain_hosts.append(host_id)
            print(Fore.RED + f"Failed to contain {hostname} ({host_id})" + Style.RESET_ALL)
            log_containment_action(hostname, host_id, "contain", "failed")

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



def main():
    config = load_config('config.yaml')     # Load the configuration

    CLIENT_ID, SECRET_ID = config['client_id'], config['client_secret']

    test_crowdstrike_connection(CLIENT_ID, SECRET_ID)    # Test the connection to the CrowdStrike API

    groups = get_host_groups(config['client_id'], config['client_secret'])     # Retrieve and display host groups
    if not groups: return  

    # User selects a group ID
    selected_group_id = input("Enter your Group ID: ")

    # Retrieve and display group members
    members = get_group_members(config['client_id'], config['client_secret'], selected_group_id)
    if not members:
        print("No members found in the selected group.")
        return

    while True:
        # Option to check containment status or lift containment
        action = input("Do you want to contain the hosts, check status, lift containment, or none? (contain/status/lift/none): ").lower()
        if action == "status":
            containment_status(members, config['client_id'], config['client_secret'])
        elif action == "contain":
            contain_hosts(members, config['client_id'], config['client_secret'])
        elif action == "lift":
            lift_containment(members, config['client_id'], config['client_secret'])
        elif action == "none":
            print("No further action taken.")
            break
        else:
            print("Invalid input. Please enter 'status', 'lift', or 'none'.")


if __name__ == "__main__":
    main()
