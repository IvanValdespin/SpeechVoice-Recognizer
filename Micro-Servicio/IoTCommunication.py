import requests
import json

class IoTCommunication():
    
    def __init__(self) -> None:
        pass

    def sendPut2(self,url,payload):
        json_data = json.dumps(payload) 
        response = requests.put(url, data=json_data)
        return response   
    
    def send_put(self,url,token,payload):

        json_data = json.dumps(payload)
        headers = {'accept':'*/*',
                   'Authentication':token,
                   'Content-Type': 'application/json'}
        
        response = requests.put(url, data=json_data,headers=headers)
        return response
    
    
    def sendGetStatus(self, url,accept = "application/json"):
        header = {
            'accept': accept
        }
        response = requests.get(url, headers=header)
        return response
    
    def sendGetMovements(self,url,token,accept = "application/json"):
        headers = {
            'accept':accept,
            'Authentication':token  
        }   
        
        response = requests.get(url,headers=headers)
        return response
    
    def sendPut(self,url,token):
       
        headers = {'accept':'*/*',
                   'Authentication':token}
        response = requests.put(url,headers=headers)
        return response
    
    def sendPost(self,url,payload):
        headers = {
            "accept":"*/*",
            "Content-Type":"application/json"
        }
        json_data = json.dumps(payload)

        response = requests.post(url,data=json_data,headers=headers)
        return response
    def sendDelete(self,url):
        headers={
            "accept":"*/*",
        }

        response = requests.delete(url,headers=headers)
        return response