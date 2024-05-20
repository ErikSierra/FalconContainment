# FalconContainment

## Overview
This project automates the containment process for a list of hosts by leveraging the CrowdStrike Falcon API. 

The code reads the list of hostnames from a configuration file, queries the API to obtain the host ID, and then contains the host using its ID. 

The project aims to simplify the security operations process by automating the containment process using the API.

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

1. Set the following fields in the YAML file to reflect the correct information
- client_id
- client_secret

2. Run the connection test script:

```bash
python APIconnectionTest.py
```

## Containing Hosts
To contain specified hosts based on a list of hostnames:
1. Create a file named computers.txt in the same directory as your script. List each hostname on a new line:
```bash
computer1
computer2
computer3
```

2. Set your YAML file to reflect the name of this .txt file 

## Run the containment script:
```bash
python Containment.py
```

## Error Handling
The scripts include basic error handling to manage issues such as:
- Handling API errors that may occur during authentication, querying and containing hosts, and printing the relevant error messages to the console.
- Handling common file I/O errors such as FileNotFoundError and printing the relevant error messages to the console.
- Checking if the configuration file has the required API credentials and file path values, exiting the script if any of them are missing.
- Checking if the hostname file exists and is not empty, exiting the script if it is missing or empty.

## Notes
- Ensure your computers.txt file is correctly formatted with one hostname per line.
- The scripts rely on the falconpy library to interact with the CrowdStrike API.
- Adjust the API credentials and file path in the YAML file as needed according to your environment. 

## Screenshots

![Screenshot of NoAPIsim.py](https://i.imgur.com/m8bBV0m.png "NoAPIsim.py")


  ## References

This project utilizes the [FalconPY](https://github.com/CrowdStrike/falconpy) library to interact with the CrowdStrike API. FalconPY is an open-source Python client for the CrowdStrike Falcon API, providing easy integration and interaction with CrowdStrike's suite of services.

For more information, documentation, and examples, visit the FalconPY GitHub repository: [FalconPY on GitHub](https://github.com/CrowdStrike/falconpy).
