import os
import yaml
import json
from falconpy import Hosts, APIError
from colorama import init, Fore, Back, Style
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
        client_id = config['api']['client_id']
        client_secret = config['api']['client_secret']
    except KeyError as e:
        messagebox.showerror("Error", f"Missing API credential in configuration file: {e}")
        sys.exit(1)

    try:
        falcon_hosts = Hosts(client_id=client_id, client_secret=client_secret)
        response = falcon_hosts.query_devices_by_filter(limit=1)
        if response["status_code"] == 200:
            messagebox.showinfo("Success", "Successfully connected to the CrowdStrike API.")
        elif response["status_code"] == 401:
            messagebox.showerror("Error", "Unauthorized: Please check your API credentials.")
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


# Function to display results in the GUI
def display_results(contained_hosts, pending_hosts, failed_hosts):
    results_window = tk.Toplevel(root)
    results_window.title("Containment Status Results")

    tk.Label(results_window, text="Contained hosts:", fg="blue").pack()
    for host in contained_hosts:
        tk.Label(results_window, text=f"- {host}", fg="blue").pack()

    tk.Label(results_window, text="\nPending containment hosts:", fg="yellow").pack()
    for host in pending_hosts:
        tk.Label(results_window, text=f"- {host}", fg="yellow").pack()

    tk.Label(results_window, text="\nNon-contained hosts:", fg="red").pack()
    for host in failed_hosts:
        tk.Label(results_window, text=f"- {host}", fg="red").pack()

    tk.Button(results_window, text="Exit", command=results_window.destroy).pack()


# Main function to start the containment status check
def start_check():
    config = load_config(CONFIG_FILE)
    test_crowdstrike_connection(config)

    rerun_check = True
    while rerun_check:
        contained_hosts = []
        pending_hosts = []
        failed_hosts = []

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
                            containment_status_response = falcon_hosts.get_device_details(ids=[host_id])
                            if containment_status_response and containment_status_response['status_code'] == 200 and containment_status_response['body']['resources']:
                                containment_status = containment_status_response['body']['resources'][0].get('status', None)
                                if containment_status == "contained":
                                    contained_hosts.append(hostname)
                                elif containment_status == "containment_pending":
                                    pending_hosts.append(hostname)
                                else:
                                    failed_hosts.append(hostname)
                            else:
                                failed_hosts.append(hostname)
                        else:
                            failed_hosts.append(hostname)
                    except APIError as e:
                        failed_hosts.append(hostname)
                    except Exception as e:
                        failed_hosts.append(hostname)
            else:
                messagebox.showerror("Error", "No hostnames found in the specified file.")
        else:
            messagebox.showerror("Error", "File path for hostnames not specified in the configuration file.")

        display_results(contained_hosts, pending_hosts, failed_hosts)

        # Ask user if they want to rerun the check again
        user_input = messagebox.askquestion("Rerun Check", "Do you want to rerun the check again?")
        if user_input == 'no':
            rerun_check = False


# GUI setup
root = tk.Tk()
root.title("CrowdStrike Host Containment Check")

frame = tk.Frame(root)
frame.pack(pady=20)

start_button = tk.Button(frame, text="Start Containment Check", command=start_check)
start_button.pack()

root.mainloop()
