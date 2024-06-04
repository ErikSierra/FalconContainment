"""
Note:
    This script is for testing purposes to attempt a mock simulation of 'Containment.py'
This script does not perform any official API containment within Crowdstrike Falcon or related resources.
Use 'Containment.py' for Crowdstrike API containment.
Refer to the GitHub repository for instructions.
"""

import os
import yaml
import sys
import tkinter as tk
from tkinter import messagebox

# Constants
CONFIG_FILE = 'config.yaml'

# Functions


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


def test_crowdstrike_connection(config, status_label):
    if not config:
        return

    conn_success = True  # Simulate successful connection
    if conn_success:
        status_label.config(text="Connection Status: Successful!", fg='#48D1CC')
        messagebox.showinfo("Success", "Successfully connected to the CrowdStrike API (simulated).")
    else:
        status_label.config(text="Connection Status: Failed!", fg='red')
        messagebox.showerror("Error", "Failed to connect to the CrowdStrike API (simulated).")


def contain_host_by_id(falcon_hosts, host_id):
    response = {
        "status_code": 200 if host_id % 2 == 0 else 202,
        "body": {"errors": [] if host_id % 2 == 0 else ["Some error"]}
    }
    return response


def display_results(success, pending, failed):
    for widget in frame.winfo_children():
        widget.destroy()

    def create_section(title, host_list, color):
        tk.Label(frame, text=title, bg='#808080', fg=color, font=('Helvetica', '14', 'bold')).pack(pady=5)
        listbox = tk.Listbox(frame, bg='#191970', fg=color, font=('Helvetica', '12'))
        listbox.pack(fill='both', padx=20, pady=5)
        for hostname in host_list:
            listbox.insert(tk.END, hostname)
        return listbox

    create_section("Successfully contained hosts:", success, '#00FFFF')
    create_section("Pending containment hosts:", pending, '#FFD700')
    create_section("Failed to contain hosts:", failed, '#FF0000')

    tk.Button(frame, text="Re-check Containment Status", command=run_containment_status, bg='#8FBC8F',
              fg='white', font=('Helvetica', '12', 'bold')).pack(pady=10, padx=10)

    tk.Button(frame, text="Exit", command=root.destroy, bg='#8FBC8F', fg='white',
              font=('Helvetica', '12', 'bold')).pack(pady=10, padx=10)


def run_containment_status():
    messagebox.showinfo("Success", "Containment status updated successfully (simulated).")


def start_containment():
    config = load_config(CONFIG_FILE)

    status_label = tk.Label(frame, text="Connection Status: Not Tested", bg='#191970', fg='white', font=('Helvetica', '18', 'bold'))
    status_label.pack(pady=10)

    if config:
        client_id = config['api']['client_id']
        client_secret = config['api']['client_secret']
        test_crowdstrike_connection(config, status_label)

        successfully_contained_hosts = []
        pending_contained_hosts = []
        failed_to_contain_hosts = []

        if 'file_path' in config:
            hostnames = read_hostnames(config['file_path'])
            if hostnames:
                for i, hostname in enumerate(hostnames):
                    host_id = i + 1
                    containment_response = contain_host_by_id(None, host_id)
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
                messagebox.showerror("Error", "No hostnames found in the specified file.")
        else:
            messagebox.showerror("Error", "File path for hostnames not specified in the configuration file.")

        display_results(successfully_contained_hosts, pending_contained_hosts, failed_to_contain_hosts)
    else:
        messagebox.showerror("Error", f"Configuration file '{CONFIG_FILE}' not found.")


# GUI setup
root = tk.Tk()
root.title("CrowdStrike Host Containment")
root.geometry("800x600")

# Load and set the background image
bg_image = tk.PhotoImage(file='background.png')
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Main frame with transparent background
frame = tk.Frame(root, bg='#808080')
frame.pack(pady=20, padx=50, fill='both', expand=True)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Title label
tk.Label(frame, text="Welcome to the CrowdStrike Host Containment Tool", bg='#191970', fg='#00BFFF', font=('Helvetica', '20', 'bold')).pack(pady=10, padx=10, fill='both')

# Start button
start_button = tk.Button(frame, text="Start Containment", command=start_containment, bg='#8FBC8F', fg='white',
                         font=('Helvetica', '16', 'bold'), pady=20, padx=20)
start_button.pack(pady=10, padx=10)

# Exit button
exit_button = tk.Button(frame, text="Exit", command=root.destroy, bg='#8FBC8F', fg='white',
                        font=('Helvetica', '16', 'bold'), pady=20, padx=20)
exit_button.pack(pady=10, padx=10)

root.mainloop()
