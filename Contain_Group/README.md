# Contain_Group

## Get_Host_Group.py

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

## GroupContainment.py

Use this file to contain a group of hosts in your Crowdstrike environment
### Usage

1. Insert your Crowdstrike API credentials into the config.yaml file in this format:\
 ```
api:
  client_id: YOUR_CLIENT_ID_HERE
  client_secret: YOUR_CLIENT_SECRET_HERE
```

2. To run the script, run the following prompt in your terminal
```
python GroupContainment.py
```


