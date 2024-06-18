# FalconContainment
[![CrowdStrike Subreddit](https://img.shields.io/badge/-r%2Fcrowdstrike-white?logo=reddit&labelColor=gray&link=https%3A%2F%2Freddit.com%2Fr%2Fcrowdstrike)](https://reddit.com/r/crowdstrike) ![GitHub releases](https://img.shields.io/github/v/release/ErikSierra/FalconContainment?label=Releases)  ![commits](https://badgen.net/github/commits/ErikSierra/FalconContainment)  ![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/ErikSierra/FalconContainment/latest?label=Commits%20since%20latest%20release) ![last-commit-badge](https://img.shields.io/github/last-commit/ErikSierra/FalconContainment) [![Repo Status](https://img.shields.io/badge/repo-active-yellow)](https://github.com/ErikSierra/FalconContainment) ![GitHub top language](https://img.shields.io/github/languages/top/ErikSierra/FalconContainment?logo=python&logoColor=white)






## Overview 🔎
This project leverages the CrowdStrike Falcon API to automate the containment process for a specified list of hosts, with the aim of simplifying security operations.

+ [Overview](#overview-)
+ [Navigation](#navigation-)
+ [Prerequisites](#prerequisites-)
+ [Notes](#notes-)
+ [References](#references-)

## Navigation 🔎
- **[FalconTests](./FalconTests)**
     - Scripts used for testing/simulating processes of the project
- **[Contain_Host](./Contain_Host)**
     - Scripts used to contain, check containment status, or lift containment on individual hosts
- **[Contain_Group](./Contain_Group)**
     - Scripts used to contain or lift containment on multiple hosts in a group

## Flowchart
![image](https://github.com/ErikSierra/FalconContainment/assets/120680439/f0150eb4-c9e0-42bf-9456-30a8c9dc297c)


## Prerequisites 🔎

1. Before using these scripts, ensure you have:
- Python 3.6 or higher installed.
- `pip` (Python package installer) installed. You can install it from [here](https://pip.pypa.io/en/stable/installation/).

2. Install the required Python packages listed in the respective requirements.txt file
   ```bash
   pip install -r requirements.txt
   
3. Obtaining API Credentials
- Before using the CrowdStrike API, you will need to obtain your client ID and client secret.
- These can be obtained by logging into the CrowdStrike Falcon console and going to System Management > API Clients, then creating a new API client. You will be provided with the client ID and client secret.
- Insert these credentials into the config.yaml files where needed (More info in sub folders)



## Notes 🔎

#### Consider (where necessary):
- Make sure you have a valid credentials for the CrowdStrike API, as you will need to provide them in the configuration file (.yaml).
- Make sure you provide the correct file path for the (computers.txt) file containing the hostnames, as it is required for the program to process the hosts.
- Review the configuration file to ensure that it contains the right information, including the client ID and client secret, which are required for authentication to the API.
- Review the limitations of the API, which may affect the success rate of containing hosts.
- Keep an eye on the overall status of containment, as well as the status of individual hosts, in your Crowdstrike tool and script's output.
  
#### Error Handling
The scripts include basic error handling to manage issues such as:
- Checking if the configuration file exists and can be read.
- Checking if the file containing the hostnames exists and can be read.
- Checking if the configuration file contains the necessary information for connecting to the CrowdStrike API.
- Checking if the connection to the CrowdStrike API is successful.
- Handling of API errors and exceptions that may occur during the connection and containment process.
- Differentiating between different HTTP response codes and errors returned by the CrowdStrike API and categorizing them as either successful, pending, or failed to contain a host.
- Printing informative error messages for easy debugging.

  

  
## Tools Used 🔎
<img src="https://i.imgur.com/JIv8Tx9.png" width="90"> <img src="https://i.imgur.com/KW5abKF.jpeg" width="150"> <img src="https://i.imgur.com/9DFxzIP.png" width="100"> <img src="https://i.imgur.com/8emdkiq.png" width="100"> <img src="https://i.imgur.com/Nj9B8hn.png" width="150"> <img src="https://i.imgur.com/qq8mtkB.png" width="200">  
## References 🔎

This project utilizes the [FalconPY](https://github.com/CrowdStrike/falconpy) library to interact with the CrowdStrike API. FalconPY is an open-source Python client for the CrowdStrike Falcon API, providing easy integration and interaction with CrowdStrike's suite of services.

For more information, documentation, and examples:

Visit the FalconPY GitHub repository: [FalconPY on GitHub](https://github.com/CrowdStrike/falconpy).

Visit the Crowdstrike Reddit: [Crowdstrike on Reddit](https://www.reddit.com/r/crowdstrike/)

Visit the FalconPY Wiki for Python: [CrowdstrikeFalconWiki](https://www.falconpy.io/Home.html).
