import os


# Function to read hostnames from a text file
def read_hostnames(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read all lines and remove extra spaces/newlines
            hostnames = [line.strip() for line in file.readlines()]
        return hostnames
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []


# Simulated function to contain a host by its ID (for testing purposes)
def contain_host_by_id_simulated(host_id):
    print(f"Simulated containment for host ID {host_id}")


# Path to your text file
file_path = 'computers.txt'  # REPLACEME

# Read hostnames from the file
hostnames = read_hostnames(file_path)
if not hostnames:
    exit("Exiting due to missing or empty hostname file.")

# Simulated host ID generation and containment
for hostname in hostnames:
    # Simulate getting a host ID (normally from the API)
    simulated_host_id = f"simulated_host_id_for_{hostname}"
    # Simulate containing the host using its ID
    contain_host_by_id_simulated(simulated_host_id)
    # Print the simulated containment response
    print(f"Simulated containment response for {hostname} ({simulated_host_id})")

'''
Note: This script is for testing purposes and does not actually interact with the CrowdStrike API.
Use 'Containment.py' for Crowdstrike API interaction
'''