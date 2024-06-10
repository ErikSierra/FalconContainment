from falconpy import HostGroup
import json

host_group = HostGroup(client_id="<YOUR CLIENT ID>", client_secret="<YOUR CLIENT SECRET>")

group_id = "ac71d7e8c876456eb10424ca96f2049d"

filter_str = "os:'Windows' and hostname:*.local and last_seen:<now>"

response = host_group.query_combined_group_members(id=group_id, filter=filter_str)

print(json.dumps(response, indent=4))