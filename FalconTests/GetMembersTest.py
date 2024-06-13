# Store the response data in a variable
response_data = falcon.query_combined_group_members(id="ac71d7e8c876456eb10424ca96f2049d",
                                                     offset=0,
                                                     limit=5000,
                                                     sort="hostname"
                                                     )

# Loop through the response data and print the details for each host
for host in response_data["resources"]:
    print("HOST DETAILS:")
    print(f"Hostname: {host.get('hostname')}")
    print(f"IP Address: {host.get('local_ip')}")
    print(f"OS: {host.get('os_version')}")
    print(f"Last Seen: {host.get('last_seen')}")
    print(f"\n")