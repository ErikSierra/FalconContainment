# FalconContainment

## Overview

This project provides scripts to:
1. Test the connection to the CrowdStrike API using environment variables for credentials.
2. Contain specified hosts by reading a list of hostnames from a text file and sending containment requests to the CrowdStrike API.

## Prerequisites

Before using these scripts, ensure you have:
- Python 3.6 or higher installed.
- `falconpy` library installed. You can install it using pip:
  ```bash
  pip install falconpy
  ```

## Usage
Testing Connection
To test the connection to the CrowdStrike API:

1. Set your CrowdStrike API credentials as environment variables:
On Windows:
```bash
set CROWDSTRIKE_CLIENT_ID=your_client_id_here
set CROWDSTRIKE_CLIENT_SECRET=your_client_secret_here
```
2. Run the connection test script:

```bash
python test_crowdstrike_connection.py
```

## Containing Hosts
To contain specified hosts based on a list of hostnames:
1. Create a file named computers.txt in the same directory as your script. List each hostname on a new line:
```bash
computer1
computer2
computer3
```

2. Set your CrowdStrike API credentials as environment variables (if not already set):

On Windows:
```bash
set CROWDSTRIKE_CLIENT_ID=your_client_id_here
set CROWDSTRIKE_CLIENT_SECRET=your_client_secret_here
```

## Run the containment script:
```bash
python contain_hosts.py
```

## Error Handling
The scripts include basic error handling to manage issues such as:
- Missing or invalid environment variables.
- File not found errors for computers.txt.
- API errors during connection or requests.

## Notes
- Ensure your computers.txt file is correctly formatted with one hostname per line.
- The scripts rely on the falconpy library to interact with the CrowdStrike API.
- Adjust the file paths and environment variable settings as needed based on your environment and setup.
  