"""
Note:
    This script is for testing purposes to attempt a mock simulation of 'Containment.py'
This script does not perform any official API containment within Crowdstrike Falcon or related resources.
Use 'Containment.py' for Crowdstrike API containment.
Refer to the GitHub repository for instructions.
"""
import yaml
import subprocess
import sys

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
    pass


# Read the configuration .yaml file
config_file_path = "config.yaml"
try:
    with open(config_file_path) as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print(f"Error: Could not find configuration file at path '{config_file_path}'")
    exit()
except Exception as e:
    print(f"Error loading configuration file at path '{config_file_path}': {e}")
    exit()
else:
    print(f"Configuration file loaded successfully from path '{config_file_path}'")

# Retrieve the file path from the configuration file
file_path = config.get("file_path")
if not file_path:
    exit("Exiting due to missing or empty file path in configuration file.")

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
    print(f"Simulated containment response for {hostname} ({simulated_host_id})")

status = input("Do you want to re-check the status of containment for these hosts? (Y/N) ")
if status.lower() == 'n':
    print("Exiting the script...")
    exit()
elif status.lower() == 'y':
    print("Running ContainmentStatus.py and checking status of hosts.")
    venv_python = sys.executable
    containment_script = "ContainmentStatus.py"
    subprocess.call([venv_python, containment_script])
else:
    print("Invalid input. Please enter Y or N.")
