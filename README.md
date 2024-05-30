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
   
3. Obtaining API Credentials
- Before using the CrowdStrike API, you will need to obtain your client ID and client secret.
- These can be obtained by logging into the CrowdStrike Falcon console and going to System Management > API Clients, then creating a new API client. You will be provided with the client ID and client secret.
- Insert these credentials in the YAML file.

## Setup
**Virtual Environment**
1. Clone this repository to your local machine/download ZIP
2. (Optional but recommended) Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

**Create .txt file**
1. Create a file named computers.txt in the same directory as your script. List each hostname on a new line that you'd like Crowdstrike to contain:
```bash
computer1
computer2
computer3
```

 - (When these hostnames are read by the script, extra spaces/newlines will automatically be removed): 

**Create .yaml file**

2. Create a file named config.yaml in the same directory as your scrip with the following information
```bash
api:
  client_id: <your client ID>
  client_secret: <your client secret>
```

- (replace backets with your own Crowdstrike API credentials)

## Testing (optional)
To test functionality/readability of .txt file:
1. Run the simulation test script:
```bash
python NoAPIsim.py
```

To test connection to Crowdstrike API:

2. Run the connection test script:

```bash
python APIconnectionTest.py
```

## Containment steps
To contain the hostnames listed in the .txt file, run the containment script:

```bash
python Containment.py
```

## Uncontainment steps
To uncontain the hostnames listed in the .txt file, run the uncontainment script:

```bash
python Lift_containment.py
```

## Error Handling
The scripts include basic error handling to manage issues such as:
- Checking if the configuration file exists and can be read.
- Checking if the file containing the hostnames exists and can be read.
- Checking if the configuration file contains the necessary information for connecting to the CrowdStrike API.
- Checking if the connection to the CrowdStrike API is successful.
- Handling of API errors and exceptions that may occur during the connection and containment process.
- Differentiating between different HTTP response codes and errors returned by the CrowdStrike API and categorizing them as either successful, pending, or failed to contain a host.
- Printing informative error messages for easy debugging.

## Notes
- Make sure you have a valid credentials for the CrowdStrike API, as you will need to provide them in the configuration file (.yaml).
- Make sure you provide the correct file path for the (.txt) file containing the hostnames, as it is required for the program to process the hosts.
- Review the configuration file to ensure that it contains the right information, including the client ID and client secret, which are required for authentication to the API.
- Review the limitations of the API, which may affect the success rate of containing hosts.
- Keep an eye on the overall status of containment, as well as the status of individual hosts, in your Crowdstrike tool and script's output. 

## Screenshots
![Screenshot of progress](https://i.imgur.com/aAZwz47.png)
![Screenshot of NoAPIsim.py](https://i.imgur.com/m8bBV0m.png "NoAPIsim.py")
![Screenshot of Containment.py](https://i.imgur.com/vAXFnpb.png)

  ## References

This project utilizes the [FalconPY](https://github.com/CrowdStrike/falconpy) library to interact with the CrowdStrike API. FalconPY is an open-source Python client for the CrowdStrike Falcon API, providing easy integration and interaction with CrowdStrike's suite of services.

For more information, documentation, and examples:

Visit the FalconPY GitHub repository: [FalconPY on GitHub](https://github.com/CrowdStrike/falconpy).

Visit the FalconPY Wiki for Python: [CrowdstrikeFalconWiki](https://www.falconpy.io/Home.html).
