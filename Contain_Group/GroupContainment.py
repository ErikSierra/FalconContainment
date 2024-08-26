import json
import sys
from falconpy import Hosts, HostGroup, APIError
from colorama import init, Fore, Style
from LoadConfig import load_config
import pandas as pd
init()
from datetime import datetime
import time

def log_containment_action(hostname, host_id, action, status):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - Hostname: {hostname}, Host ID: {host_id}, Action: {action}, Status: {status}\n"
    with open("group_containment_log.txt", "a") as log_file:
        log_file.write(log_message)


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
    

# Function to check containment status
def containment_status(hosts, client_id, client_secret):
    falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
    
    for host_id in hosts:
        result = falcon_hosts.get_device_details(ids=host_id)
        if result["status_code"] == 200:
            status = result["body"]["resources"][0]["status"]
            hostname = result["body"]["resources"][0]["hostname"]
            print(f"Hostname: {hostname}, ID: {host_id} ==> Status: {status}")
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

    time.delay(60)

    for host_id in hosts:
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
         


# Function to lift containment for hosts
def lift_containment(hosts, client_id, client_secret):
    falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
    successfully_uncontained_hosts = []
    pending_uncontained_hosts = []
    failed_to_uncontain_hosts = []

    for host_id in hosts:
        uncontain_host_by_id(falcon_hosts, host_id)

    for host_id in hosts:
        result = falcon_hosts.get_device_details(ids=host_id)

        if result["status_code"] == 200:
            status = result["body"]["resources"][0]["status"]
            hostname = result["body"]["resources"][0]["hostname"]
            if status == "contained":
                failed_to_uncontain_hosts.append([hostname, host_id])
            elif status == "normal":
                successfully_uncontained_hosts.append([hostname, host_id])
            else:
                pending_uncontained_hosts.append([hostname, host_id])
        else:
            print(result["body"]["errors"])

    print("SuccessFully lifted: \n")
    for i in range(len(successfully_uncontained_hosts)):
        name, id = successfully_uncontained_hosts[i]
        print("Host name: ", name, " Host id: ", id)
        log_containment_action(name, id, "normal")
 
    print("Pending uncontainment: \n")
    for i in range(len(pending_uncontained_hosts)):
        name, id = pending_uncontained_hosts[i]
        print("Host name: ", name, " Host id: ", id)
        log_containment_action(name, id, "pending")

    print("Failed uncontainment: \n")
    for i in range(len(failed_to_uncontain_hosts)):
        name, id = failed_to_uncontain_hosts[i]
        print("Host name: ", name, " Host id: ", id)
        log_containment_action(name, id, "contained")






def main():
    config = load_config('config.yaml')

    CLIENT_ID = config['client_id']
    CLIENT_SECRET = config['client_secret']

    groups = get_host_groups(CLIENT_ID, CLIENT_SECRET)
    if not groups: return  

    # User selects a group ID
    selected_group_id = input("Enter your Group ID: ")

    # Retrieve and display group members
    members = get_group_members(CLIENT_ID, CLIENT_SECRET, selected_group_id)
    if not members:
        print("No members found in the selected group.")
        return

    while True:
        action = input("Do you want to: \n1. contain the hosts \"contain\" \n2. check status \"status\" \n3. lift containment \"lift\" \n4. none \"none\" \n").lower()

        if action == "status":
            containment_status(members, CLIENT_ID, CLIENT_SECRET)
        elif action == "contain":
            contain_hosts(members, CLIENT_ID, CLIENT_SECRET)
        elif action == "lift":
            lift_containment(members, CLIENT_ID, CLIENT_SECRET)
        elif action == "none":
            print("No further action taken.")
            break
        else:
            print("Invalid input. Please enter 'status', 'lift', or 'none'.")


if __name__ == "__main__":
    main()