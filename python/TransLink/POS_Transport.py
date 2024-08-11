from requests import request

class POS_Transport():

    def SendCommandToPOS(self, dict : dict):
        responce = request('POST', url='')
