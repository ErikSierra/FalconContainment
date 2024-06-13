from falconpy import HostGroup

# Do not hardcode API credentials!
falcon = HostGroup(client_id=CLIENT_ID,
                   client_secret=CLIENT_SECRET
                   )

response = falcon.query_combined_group_members(id="ac71d7e8c876456eb10424ca96f2049d",
                                               filter="hostname",
                                               offset=0,
                                               limit=5000,
                                               sort="hostname"
                                               )
print(response)
