from GetToken import getToken   
from GetDeviceId import getDeviceId
from GetRtrSessionId import initiateRtrSession
from RemoveAdminRights import removeAdminRights

#gets token
token = getToken
if token: print('Authentication successful')
else:
    print('Authentication failed:')
    exit()


#gets device id
hostname = input("Please input target hostname: ") 
device_id = getDeviceId(token, hostname)


#gets session id
session_id = initiateRtrSession(token, device_id)


#removes admin rights
username = input("Please enter target device username: ")
result = removeAdminRights(token, session_id, username)


#prints final result
print("Command Execution Result:", result)
