# FalconContainment

## Overview

This project provides scripts to:
1. Test the connection to the CrowdStrike API using environment variables for credentials.
2. Contain specified hosts by reading a list of hostnames from a text file and sending containment requests to the CrowdStrike API.

## Prerequisites

1. Before using these scripts, ensure you have:
- Python 3.6 or higher installed.
- `pip` (Python package installer) installed. You can install it from [here](https://pip.pypa.io/en/stable/installation/).

2. Install the required Python packages listed in the requirements.txt file
   ```bash
   pip install -r requirements.txt

## Setup

1. Clone this repository to your local machine.
2. (Optional but recommended) Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
  
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

## Screenshots

![Screenshot of My Image](https://i.imgur.com/m8bBV0m.png "NoAPIsim.py")


  ## References

This project utilizes the [FalconPY](https://github.com/CrowdStrike/falconpy) library to interact with the CrowdStrike API. FalconPY is an open-source Python client for the CrowdStrike Falcon API, providing easy integration and interaction with CrowdStrike's suite of services.

For more information, documentation, and examples, visit the FalconPY GitHub repository: [FalconPY on GitHub](https://github.com/CrowdStrike/falconpy).
