## Falcon Tests

These files are used only for testing the functionality of the FalconContainment process. Each .py tests different parts of the process in order to minimize errors during official use.

### APIconnectionTest.py

This script is designed to test the connection to the Crowdstrike API and to read hosts provided in the computers.txt file.

#### Usage

1. Install the necessary packages by running the following prompt in your terminal
pip install -r requirements.txt


2. Use the config.yaml file and insert your API credentials and the file path to the computers.txt file. The file should be structured as follows:
api: client_id: YOUR_CLIENT_ID client_secret: YOUR_CLIENT_SECRET file_path: computers.txt


3. Run the script by navigating to the directory where the file is located and running the following prompt in your terminal
python APIconnectionTest.py


*** Please note that this script is for testing purposes only and should not be used for any official API containment within Crowdstrike Falcon or related resources. Use 'Containment.py' for Crowdstrike API containment. Refer to the GitHub repository for instructions.***

For details on the functions within the script, please refer to the comments within the code.
