from typing import List
from TransLink import Event, Events

class PosEmulator:

    def __init__(self, posName: str):
        self.text = "WELCOME"
        self.queue: List = []
        self.lastReceipt: str = ""
        self.posName: str = posName

        self.licenseToken = "e034d5a6cf3212826c57f35cffb103905afe5936/f86419d06688b6336ddfe68dc00c214b9b83fb10"

        self.accessToken = "7C65891202494794599402621701736360258001"

    def getConfig(self):
        return {"name": self.posName,
                "text": self.text,
                "queue": self.queue,
                "lastReceipt": self.lastReceipt
                }

    def getAccessToken(self):
        return self.accessToken

    def openpos(self, licenseToken):
        if licenseToken != self.licenseToken:
            return unAuthorizationResultBedkey()

        result = {
            "accessToken": self.accessToken
        }

    def closepos(self, accessToken : str = ""):
        return {
            "resultCode": "OK",
            "resultMessage": "closepos was sent",
            "resultTime": ""
        }

    def getsoftwareversions(self):
        return {
            "compatibleApiVersions": ["v101", "v102", "v103"],
            "releaseVersion": "2.3.16.0"
        }

    def getEvent(self):
        return Events.getEvent()

    def executeposcmd(self, commandname, body):
        result = {
            "resultCode": "OK",
            "resultMessage": f"{commandname} was sent successfull!",
            "resultTime": ""
        }
        match commandname:
            case "UNLOCKDEVICE":

                Events.createevent_ONCARD(body)
                print(body)
            case "GETPOSSTATUS":
                print(body)
                result["resultMessage"] = "Status is ok"

            case "LOCKDEVICE":
                print(body)
            case "AUTHORIZE":
                Events.createevent_AUTORISE_ONPRINT(body)
                Events.createevent_ONTRNSTATUS(body)
                print(body)
            case "CLOSEDAY":
                Events.createevent_CLOSEDAY_ONPRINT(body)
                print(body)
            case "PRINTTOTALS":
                Events.createevent_PRINTTOTALS_ONPRINT(body)
                print(body)

        return result


#def checkAuth(authorization: str):
#    return accessToken in authorization


def unAuthorizationResult():
    result = {
        "resultCode": "NOT_INITILIAZED",
        "resultMessage": "UnAuthorization Result",
        "resultTime": ""
    }
    return result


def unAuthorizationResultBedkey():
    result = {
        "resultCode": "NOT_INITILIAZED",
        "resultMessage": "key error",
        "resultTime": ""
    }
    return result