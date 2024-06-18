# Contain_Group
For the following files, please ensure the correct Crowdstrike API credentials are inputted in the [config.yaml](./config.yaml) file
+ [GetHostGroup.py](https://github.com/ErikSierra/FalconContainment/blob/main/Contain_Group/README.md#gethostgrouppy-)
+ [GetGroupMembers.py](https://github.com/ErikSierra/FalconContainment/blob/main/Contain_Group/README.md#getgroupmemberspy-)
+ [GroupContainment.py](https://github.com/ErikSierra/FalconContainment/tree/main/Contain_Group#groupcontainmentpy)

## GetHostGroup.py 🔎

Use this file to retrieve information on groups in your Crowdstrike environment

### Usage

1. To run the script, run the following prompt in your terminal

```
python3 Get_Host_Group.py -k FALCON_CLIENT_ID -s FALCON_CLIENT_SECRET
```

2. If you'd like to output the results to a txt file for easier visibility, please run the following prompt in your terminal
```
python3 Get_Host_Group.py -k FALCON_CLIENT_ID -s FALCON_CLIENT_SECRET > FileName.txt
```
#### Example result (method 2)
![image](https://github.com/ErikSierra/FalconContainment/assets/120680439/b479843b-43bd-453b-9406-3b9a1a6137c5)


## GetGroupMembers.py

Use this file to retrieve information on members in your provided group in your Crowdstrike environment
### Usage

1. Insert your group ID into the script
   (GROUP_ID = '123456789')
   
3. To run the script, run the following prompt in your terminal

  ```
  python GetGRoupMembers.py
  ```
  
  If you'd like to output the results to a txt file for easier visibility, please run the following prompt in your terminal
  ```
  python GetGroupMembers.py > FileName.txt
  ```

#### Example result (method 2)
![image](https://github.com/ErikSierra/FalconContainment/assets/120680439/a85084a7-d74c-4e4b-8de1-646d5b4b72c2)

## GroupContainment.py

Use this file to contain a group of hosts in your Crowdstrike environment
### Usage

1. Insert your Crowdstrike API credentials into the [config.yaml](./config.yaml) file in this format:
 ```
api:
  client_id: YOUR_CLIENT_ID_HERE
  client_secret: YOUR_CLIENT_SECRET_HERE
```

2. To run the script, run the following prompt in your terminal
```
python GroupContainment.py
```
#### Example result 
![image](https://github.com/ErikSierra/FalconContainment/assets/120680439/a82ca025-7502-476c-bd68-c2da35cde17a)


