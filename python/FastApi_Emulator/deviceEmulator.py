from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

#1from .deviceEmulator import createevent_CLOSEDAY_ONPRINT


class OpenPosBody(BaseModel):
    licenseToken: str = "",
    alias: str = "",
    username: str = "",
    password: str = ""


class CommandName(BaseModel):
    command: str = ""


class CommandParams(BaseModel):
    posOperation: str = ''
    amount: int = 0
    currencyCode: str = ''
    documentNr: str = ''


class CommandBody(BaseModel):
    header: CommandName
    params: CommandParams


app = FastAPI()
url = "/v107"
licenseToken = "e034d5a6cf3212826c57f35cffb103905afe5936/f86419d06688b6336ddfe68dc00c214b9b83fb10"

accessToken = "7C65891202494794599402621701736360258001"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=accessToken)
eventlist = []


@app.get("/")
def read_root():
    return {"Hello": "TransLink POS emulator - see docs http://127.0.0.1:6678/docs#/"}


@app.post(url + "/openpos")
def openpos(body: OpenPosBody):
    """codumentation of this function"""

    if body.licenseToken != licenseToken:
        return unAuthorizationResultBedkey()

    result = {
        "accessToken": accessToken
    }
    return result


@app.post(url + "/closepos")
def closepos(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    print("Authorization ", token)

    result = {
        "resultCode": "OK",
        "resultMessage": "closepos was sent",
        "resultTime": ""
    }
    return result


@app.get(url + "/getsoftwareversions")
def getsoftwareversions(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    if token == "":
        print('Empty token')

    result = {
        "compatibleApiVersions":  ["v101", "v102", "v103"],
        "releaseVersion": "2.3.16.0"
    }
    return result


@app.get(url + "/getEvent")
def getEvent(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:

    if token == "":
        print('Empty token')

    result = {
                "eventName": None,
                "properties": None,
                "result": {
                    "resultCode": "OK",
                    "resultMessage": "Queue empty.",
                    "resultTime": "20240819052119"
                }
            }


    if len(eventlist) > 0:
        result = eventlist.pop(0)

    return result


@app.post(url + "/executeposcmd")
def executeposcmd(token: Annotated[str, Depends(oauth2_scheme)], body: CommandBody) -> dict:
    print("token ", token)
    print("BODY ", body)
    commandName = body.header.command
    params = body.params
    print(f"commandName={commandName}")
#   print(f"params={params}")

    match commandName:
        case "UNLOCKDEVICE":
            eventlist.append(createevent_ONCARD(body))
        case "LOCKDEVICE":
            ...
        case "AUTHORIZE":
            eventlist.append(createevent_AUTORISE_ONPRINT(body))
            eventlist.append(createevent_ONTRNSTATUS(body))

        case "CLOSEDAY":
            eventlist.append(createevent_CLOSEDAY_ONPRINT(body))

    result = {
        "resultCode": "OK",
        "resultMessage": f"{commandName} was sent",
        "resultTime": ""
    }
    return result

def createevent_ONCARD(body):

     result = {"eventName": "ONCARD",
     "properties": {
         "hash": "629E3724910B9869C6551E1FCA03478C1DD9F5C7",
         "track1": "",
         "track2": "",
         "track3": "",
         "PAN": "414051******2480",
         "cardType": "VISA",
         "currencyCode": "981",
         "additionalCurrencyCodes": None,
         "cardTechs": None,
         "cardData": [],
         "UID": None,
         "loyCard": False,
         "allowAuthorize": True,
         "allowPreAuthorize": True,
         "allowRefund": True,
         "fullAmountOnly": False,
         "noDiscounts": False,
         "reqPAN4Digit": False,
         "reqOriginalData": False,
         "reqOriginalRRN": False,
         "allowCashBack": True,
         "allowInstallmentIssuer": True,
         "allowInstallmentMerchant": False,
         "allowInstallmentAcquirer": False,
         "installmentFormIssuer": None,
         "installmentFormMerchant": None,
         "installmentFormAcquirer": None},
     "result": {
         "resultCode": "OK",
         "resultMessage": "Operation completed successfully",
         "resultTime": "20240808123943"}
     }
     return result


def createevent_CLOSEDAY_ONPRINT(body):

    result = {
        "eventName": "ONPRINT",
        "properties": {
            "receiptText": "          End of Day report\n--------------------------------------\n\n\n              TEST BANK\nMerchant: Ashburn International GE\nAddress: Adress str. 17\n\nTerminal ID: 1C000001\n\nSet 1 \"Visa\"                       GEL\nTransactions:    1                1.00\nCancelled:       0                0.00\nTotal:           1                1.00\n\nSet 2 \"Mastercard\"                 GEL\nTransactions:    1                2.00\nCancelled:       0                0.00\nTotal:           1                2.00\n\nTotal                              GEL\nTransactions:    2                3.00\nCancelled:       0                0.00\nTotal:           2                3.00\n______________________________________\nOK                 2024-08-08 13:32:33\n\n",
            "documentNr": ""
            },
        "result": {
            "resultCode": "OK",
            "resultMessage": "Operation completed successfully",
            "resultTime": "20240808143234"
        }
    }
    return result

def createevent_AUTORISE_ONPRINT(body):
    result = {
        "eventName":"ONPRINT",
        "properties":{"receiptText":"\\mc\n\\imRANDOM.IMG\n  \n        Ashburn International\n       Tbilisi, Adress str. 17\n       Ashburn International GE\n  \n           ბარათით გადახდა\n                ყიდვა\n  \n              უკონტაქტო\n\nქვითარი:                        100119\nტერმინალი:                    1C000001\nმოვაჭრე:                     1C1000001\nRRN:                      4221RR100119\nთარიღი და დრო:     2024.08.08 11:39:41\nბარათი:               414051******2480\n                                  Visa\n                                     /\nAID:A0000000031010 \n  \nთანხის ოდენობა:               1.00 GEL\n  \nავტორიზაციის კოდი:      79649Z     T:1\n  \n  \n000 OK\n  \n            დადასტურებულია\n\\cl\n\\imRANDOM.IMG\n  \n        Ashburn International\n       Tbilisi, Adress str. 17\n       Ashburn International GE\n  \n           ბარათით გადახდა\n                ყიდვა\n  \n              უკონტაქტო\n\nქვითარი:                        100119\nტერმინალი:                    1C000001\nმოვაჭრე:                     1C1000001\nRRN:                      4221RR100119\nთარიღი და დრო:     2024.08.08 11:39:41\nბარათი:               414051******2480\n                                  Visa\n                                     /\nAID:A0000000031010 \n  \nთანხის ოდენობა:               1.00 GEL\n  \nავტორიზაციის კოდი:      79649Z     T:1\n  \n  \n000 OK\n  \n            დადასტურებულია\n","documentNr":"307855"},"result":{"resultCode":"OK","resultMessage":"Operation completed successfully","resultTime":"20240808123946"}
    }
    return result

def createevent_ONTRNSTATUS():
    result = {
        "eventName":"ONTRNSTATUS",
        "properties":{"operationId":"OF8B2CFCCBF6E71CB","amountAuthorized":100,"documentNr":"307855","cryptogram":None,"authCode":"79649Z","RRN":"4221RR100119","STAN":"119","cardType":"VISA","amountAdditional":None,"text":"000 - OK","state":"Approved","authorizationState":"","cardName":"Visa","APN":"Visa Credit","AID":"A0000000031010","CVMApplied":["NoCVM"],"authCenterName":"TEST BANK","tranSourceMedia":"EmvContactless","PAN":"414051******2480","DCCResult":"DccNotOffered","EcrData":""},"result":{"resultCode":"OK","resultMessage":"Operation completed successfully","resultTime":"20240808123947"}
    }
    return result


def checkAuth(authorization: str):
    return accessToken in authorization


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
