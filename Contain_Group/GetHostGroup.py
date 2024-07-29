#THIS SCRIPT IS TO RETRIEVE AND LIST ALL HOST GROUPS IN CROWDSTRIKE. USE THE FOLLOWING COMMAND:

from falconpy import APIHarnessV2
import pandas as pd
from LoadConfig import load_config # loads config.yaml

config = load_config('config.yaml')

# Create our base authentication dictionary (parent / child)
auth = {
    "client_id": config['client_id'],
    "client_secret": config['client_secret'],
    "pythonic": True
}
    
groupNames, groupIds, groupDescription= list(), list(), list()
    
with APIHarnessV2(**auth) as sdk:
    results = sdk.command("queryCombinedHostGroups")
        
    for result in results:
        groupNames.append(result['name'])
        groupIds.append(result['id'])
        groupDescription.append(result.get('description', 'N/A'))

    # Create the DataFrame
    data = {
        'Group Name': groupNames,
        'Group Ids': groupIds,
        'Description': groupDescription
    }
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame(data)
        
    # Print the DataFrame
    print("\n", df, "\n")
        
df.to_csv('HostGroups.csv')