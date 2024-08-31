import urllib3
from requests import post, get
from .settings import Settings
from .types import ResultType
from typing import Any
import json
import sys



class POS_Transport():

    _settings : Settings
    _accessToken : str = ''

    def __init__(self, settings):
        self._settings = settings

    def GetSettings(self):
        return self._settings

    def SetAccessToken(self, accessToken : str):
        self._accessToken = accessToken
    
    def SendCommandToPOS(self, commandName : dict, params : dict):

        functionName = 'executeposcmd'
        url = f'{self._settings.terminalURL}/{self._settings.apiVersion}/{functionName}'

        headers = {
            'Content-Type': 'application/json'
        }
        if self._accessToken != "":
            headers['Authorization'] = "Bearer " + self._accessToken

        commandStructure = {
            'header' : {
                'command' : commandName
            }
        }

        if len(params)>0:
            commandStructure['params'] = params.copy()

        responce = self.SendToPOS(functionName, body=commandStructure)

        if responce['status_code'] == 200:
            ...
        
        result = ResultType()

        return result

    def SendToPOS(self, functionName : str, method : str = 'POST', body : Any|None = None):

        result = {"status_code" : 0,
                  "body" : "",
                  "json" : {}
                  }
        
        responce = None

        url = f'{self._settings.terminalURL}/{self._settings.apiVersion}/{functionName}'

        headers = {
            'Content-Type': 'application/json'
        }
        if self._accessToken != "":
            headers['Authorization'] = f"Bearer {self._accessToken}"

        try:
            if method == 'GET':
                responce = get(url=url,headers=headers)
            elif method == 'POST':
                responce = post(url=url, headers=headers, json=body)

            result['status_code'] = responce.status_code
            result['body'] = responce.text

            if responce.status_code == 200:
                result['json'] = responce.json()
        except ConnectionError as err:
            result['status_code'] = -1
            print('ConnectionError')

        except ValueError as err:
            result['status_code'] = -1
            print('ERROR')

        except urllib3.exceptions.MaxRetryError as err:
            result['status_code'] = -1
            print('MaxRetryError')

        return result