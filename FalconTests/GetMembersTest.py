from falconpy.hosts import Hosts
from falconpy import HostGroup
from Group_Containment.GetGroupMembers import falcon

group_id = "<group_id>"  # Replace <group_id> with the actual group ID you want to filter by
filter_string = f"group_id:'{group_id}'"

returned = falcon.query_devices_by_filter(
    sort="hostname.asc"
)

print(returned)

group_id = "<group_id>"  # Replace <group_id> with the actual group ID you want to filter by
filter_string = f"group_id:'{group_id}'"
results = falcon.query_devices_by_filter(filter=filter_string)
