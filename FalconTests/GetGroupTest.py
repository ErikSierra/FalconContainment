from falconpy import HostGroup

# Do not hardcode API credentials!
falcon = HostGroup(client_id=CLIENT_ID,
                   client_secret=CLIENT_SECRET
                   )

response = falcon.query_combined_host_groups(filter="string",  # Query to filter host groups
                                             offset=0,
                                             limit=5000,
                                             sort="string"
                                             )
print(response)
