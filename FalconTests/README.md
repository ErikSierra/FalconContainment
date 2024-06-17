## Falcon Tests

These files are used only for testing the functionality of the FalconContainment process. Each .py tests different parts of the process in order to minimize errors during official use.

For all files, install the necessary packages by running the following prompt in your terminal
```
pip install -r requirements.txt
```
### APIconnectionTest.py

This script is designed to test the connection to the Crowdstrike API and to read hosts provided in the computers.txt file.

#### Usage
1. Use the config.yaml file and insert your API credentials and the file path to the computers.txt file. The file should be structured as follows:
api: client_id: YOUR_CLIENT_ID client_secret: YOUR_CLIENT_SECRET file_path: computers.txt


2. Run the script by navigating to the directory where the file is located and running the following prompt in your terminal
python APIconnectionTest.py



### GetMembersTest.py

This script is used to test retrieval of members of a group in your crowdstrike environment

#### Usage

1. Use the config.yaml file and insert your API credentials and the file path to the computers.txt file. The file should be structured as follows:
api: client_id: YOUR_CLIENT_ID client_secret: YOUR_CLIENT_SECRET file_path: computers.txt

2. Insert your group ID from crowdstrike into the "GROUP_ID" field in the script

3. Run the script by navigating to the directory where the file is located and running the following prompt in your terminal
```
python GetMembersTest.py
```

### Gui test.py

This script is used to test a GUI window creation. Use this script as a start if you would like to customize the outputted display for any scripts instead of reading results from the terminal. 
#### Usage

1. Run the script by navigating to the directory where the file is located and running the following prompt in your terminal
```
python Gui test.py
```

### GroupContainSim.py

This script is used to simulate containment on a group in your Crowdstrike environment. This will not actually interact with your Crowdstrike environment or anything inside

#### Usage

1. Run the script by navigating to the directory where the file is located and running the following prompt in your terminal
```
python GroupContainmentSim.py
```


### NoAPIsim.py

This script is used to simulate containment on a list of hosts defined in the computers.txt file. This will not actually interact with your Crowdstrike environment or anything inside

#### Usage

1. Run the script by navigating to the directory where the file is located and running the following prompt in your terminal
```
python NoAPIsim.py
```



