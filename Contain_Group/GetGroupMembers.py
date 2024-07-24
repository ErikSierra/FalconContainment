from falconpy import HostGroup
import pandas as pd 
from LoadConfig import load_config # loads config.yaml

config = load_config('config.yaml')

hosts = open("Hosts.txt", "w") #open a text file named hosts
GROUP_ID = input("Please enter group ID: ") #get group id from user

falcon = HostGroup(client_id = config['client_id'], client_secret = config['client_secret']) # Initialize the API harness

# Function to print the names and IDs of the members of a host group and export to Hosts.txt
def list_host_group_members(group_id):
    try:
        response = falcon.query_combined_group_members(id=group_id, limit=5000)
        if response['status_code'] != 200:
            print(f"Error fetching group members: {response.get('errors', 'Unknown error')}")
            return
        
        # Extract and print hostnames and IDs
        members = response['body']['resources']
        hostNames, hostIds = list(), list()

        for member in members:
            hostNames.append(member.get('hostname', 'Unknown hostname'))
            hostIds.append(member.get('device_id', 'Unknown ID'))

        data = {
            'Host_Name' : hostNames,
            'HostIds' : hostIds
        }
        pd.set_option('display.max_rows', None)
        df = pd.DataFrame(data) 
        print("\n", df, "\n")
        hosts.write(str(df))

    except Exception as e:
        print(f"An error occurred: {e}")

list_host_group_members(GROUP_ID) # List the members of the specified host group

hosts.close()