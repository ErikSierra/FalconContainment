# Contain_Host

These files are used for the following purposes:
- Contain host(s)
- Check containment status
- Lift containment

## Containment.py
Use this file to contain one or more hosts in your Crowdstrike environment

### Usage

1. Insert your Crowdstrike API credentials into the YAML file in this format:
  api:
    client_id: <your client ID>
    client_secret: <your client secret>
2. List the names of your hosts from your crowdstrike environment in the computers.txt file in this format:
  Computer 1
  Computer 2
  Computer 3

3. Execute the script by running the following prompt in your terminal 
```
python Containment.py
```
4. Note the resulting output in the terminal and follow any further intructions provided in the terminal

**THIS SCRIPT INTERACTS WITH YOUR CROWDSTRIKE ENVIRONMENT. PLEASE PROCEED WITH CAUTION**

## ContainmentStatus.py
Use this file to check the containment status on one or more hosts in your Crowdstrike environment

### Usage
1. Insert your Crowdstrike API credentials into the YAML file in this format:
  api:
    client_id: <your client ID>
    client_secret: <your client secret>
2. List the names of your hosts from your crowdstrike environment in the computers.txt file in this format:
  Computer 1
  Computer 2
  Computer 3

3. Execute the script by running the following prompt in your terminal 
```
python ContainmentStatus.py
```
4. Note the resulting output in the terminal and follow any further intructions provided in the terminal

## Lift_containment.py
Use this file to lift containment on one or more hosts in your Crowdstrike environment
### Usage
1. Insert your Crowdstrike API credentials into the YAML file in this format:
  api:
    client_id: <your client ID>
    client_secret: <your client secret>
2. List the names of your hosts from your crowdstrike environment in the computers.txt file in this format:
  Computer 1
  Computer 2
  Computer 3

3. Execute the script by running the following prompt in your terminal 
```
python Lift_containment.py
```
4. Note the resulting output in the terminal and follow any further intructions provided in the terminal

