from falconpy import HostGroup

# Do not hardcode API credentials!
falcon = HostGroup(client_id=CLIENT_ID,
                   client_secret=CLIENT_SECRET
                   )

response = falcon.query_combined_group_members(id="string",
                                               offset=integer,
                                               limit=integer,
                                               sort="string"
                                               )
print(response)

