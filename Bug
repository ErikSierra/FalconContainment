import os
import yaml
import json
import sys
from falconpy import Hosts, RealTimeResponse, APIError
from colorama import init, Fore, Back, Style
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, filedialog

init()

# Constants
CONFIG_FILE = 'config.yaml'


# Function to load configuration
def load_config(file_path):
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", f"Configuration file '{file_path}' not found.")
        sys.exit(1)

    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
            return config
    except yaml.YAMLError as e:
        messagebox.showerror("Error", f"Error reading configuration file: {e}")
        sys.exit(1)


# Function to read hostnames from a text file
def read_hostnames(file_path):
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", f"The file '{file_path}' was not found.")
        sys.exit(1)
    try:
        with open(file_path, 'r') as file:
            hostnames = [line.strip() for line in file.readlines()]
        return hostnames
    except Exception as e:
        messagebox.showerror("Error", f"Error reading '{file_path}': {e}")
        sys.exit(1)


# Function to test the connection to the CrowdStrike API
def test_crowdstrike_connection(config):
    if not config:
        return

    try:
        # API credentials
        client_id = config['api']['client_id']
        client_secret = config['api']['client_secret']
    except KeyError as e:
        messagebox.showerror("Error", f"Missing API credential in configuration file: {e}")
        sys.exit(1)

    # Connect to the CrowdStrike API
    try:
        falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
        # Perform a simple request to verify the connection
        response = falcon_hosts.query_devices_by_filter(limit=1)
        if response["status_code"] == 200:
            messagebox.showinfo("Success", "Successfully connected to the CrowdStrike API.")
        elif response["status_code"] == 401:
            messagebox.showerror("Error", "Unauthorized: Please check your API credentials in the .yaml file.")
            sys.exit(1)
        else:
            messagebox.showerror("Error", f"Failed to connect to the CrowdStrike API. Status code: {response['status_code']}")
            sys.exit(1)
    except APIError as e:
        messagebox.showerror("Error", f"APIError during authentication: {e.message}")
        sys.exit(1)
    except Exception as e:
        messagebox.showerror("Error", f"Error during API connection: {e}")
        sys.exit(1)


# Function to contain a host by its ID
def contain_host_by_id(falcon_hosts, host_id):
    try:
        response = falcon_hosts.perform_action(action_name="contain", ids=[host_id])
        return response
    except APIError as e:
        messagebox.showerror("Error", f"APIError containing host ID {host_id}: {e.message}")
    except Exception as e:
        messagebox.showerror("Error", f"Error containing host ID {host_id}: {e}")
        return None


# Function to display results in the GUI
def display_results(success, pending, failed):
    results_window = tk.Toplevel(root)
    results_window.title("Containment Results")

    tk.Label(results_window, text="Successfully contained hosts:", fg="blue").pack()
    for host in success:
        tk.Label(results_window, text=f"- {host}", fg="blue").pack()

    tk.Label(results_window, text="\nPending containment hosts:", fg="yellow").pack()
    for host in pending:
        tk.Label(results_window, text=f"- {host}", fg="yellow").pack()

    tk.Label(results_window, text="\nFailed to contain hosts:", fg="red").pack()
    for host in failed:
        tk.Label(results_window, text=f"- {host}", fg="red").pack()

    tk.Label(results_window, text="\n").pack()
    tk.Button(results_window, text="Re-check Containment Status", command=run_containment_status).pack()
    tk.Button(results_window, text="Exit", command=results_window.destroy).pack()


# Function to run ContainmentStatus.py
def run_containment_status():
    venv_python = sys.executable
    containment_script = "ContainmentStatus.py"
    subprocess.call([venv_python, containment_script])


# Main function to start the containment process
def start_containment():
    config = load_config(CONFIG_FILE)
    test_crowdstrike_connection(config)

    successfully_contained_hosts = []
    pending_contained_hosts = []
    failed_to_contain_hosts = []

    if config and 'file_path' in config:
        hostnames = read_hostnames(config['file_path'])
        if hostnames:
            client_id = config['api']['client_id']
            client_secret = config['api']['client_secret']

            try:
                falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
            except APIError as e:
                messagebox.showerror("Error", f"APIError during authentication: {e.message}")
            except Exception as e:
                messagebox.showerror("Error", f"Error during API connection: {e}")

            for hostname in hostnames:
                try:
                    response = falcon_hosts.query_devices_by_filter(filter=f"hostname:'{hostname}'")
                    if response["status_code"] == 200 and "resources" in response["body"] and response["body"]["resources"]:
                        host_id = response["body"]["resources"][0]
                        containment_response = contain_host_by_id(falcon_hosts, host_id)
                        if containment_response:
                            if containment_response["status_code"] == 200 and not containment_response["body"].get("errors"):
                                successfully_contained_hosts.append(hostname)
                            elif containment_response["status_code"] == 202 and not containment_response["body"].get("errors"):
                                pending_contained_hosts.append(hostname)
                            else:
                                failed_to_contain_hosts.append(hostname)
                        else:
                            failed_to_contain_hosts.append(hostname)
                    else:
                        failed_to_contain_hosts.append(hostname)
                except APIError as e:
                    failed_to_contain_hosts.append(hostname)
                except Exception as e:
                    failed_to_contain_hosts.append(hostname)
        else:
            messagebox.showerror("Error", "No hostnames found in the specified file.")
    else:
        messagebox.showerror("Error", "File path for hostnames not specified in the configuration file.")

    display_results(successfully_contained_hosts, pending_contained_hosts, failed_to_contain_hosts)


# GUI setup
root = tk.Tk()
root.title("CrowdStrike Host Containment")

frame = tk.Frame(root)
frame.pack(pady=20)

start_button = tk.Button(frame, text="Start Containment", command=start_containment)
start_button.pack()

root.mainloop()
