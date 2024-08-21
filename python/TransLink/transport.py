from requests import post, get
from .settings import Settings
import json

class POS_Transport():

    _settings : Settings
    _accessToken : str = ''

    def __init__(self, settings):
        self._settings = settings

    def SetaccessToken(self, accessToken : str):
        self._accessToken = accessToken
    def SendCommandToPOS(self, commandName : dict, params : dict):

        functionName = 'executeposcmd'
        url = f'{self._settings.terminalURL}/{self._settings.apiVersion}/{functionName}'

        headers = {
            'Content-Type': 'application/json'
        }

        commandStructure = {
            'header' : {
                'command' : commandName
            }
        }

        if len(params)>0:
            commandStructure['params'] = params.copy()

        responce = self.SendToPOS()

        if responce.status_code != 200:
            ...

        return responce.json()

    def SendToPOS(self, functionName : str, method : str = 'POST', body : str = ''):

        result = {}

        url = f'{self._settings.terminalURL}/{self._settings.apiVersion}/{functionName}'

        headers = {
            'Content-Type': 'application/json'
        }
        #try:
        if method == 'GET':
            responce = get(url=url,headers=headers)
        elif method == 'POST':
            responce = post(url=url, headers=headers, json=body)

        if responce.status_code != 200:
            result = responce.json()

        #except :
        #    ...
        #finally:
        #    ...




        return result