from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from TransLink import Event, Events
from pprint import pprint

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


@app.get("/")
def read_root():
    return {"Hello": "TransLink POS emulator - see docs http://127.0.0.1:6678/docs#/"}


@app.post(url + "/openpos")
def openpos(body: OpenPosBody):
    """documentation of this function"""

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


@app.get(url + "/getevent")
def getevent(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:

    if token == "":
        print('Empty token')

    return Events.getEvent()


@app.post(url + "/executeposcmd")
def executeposcmd(token: Annotated[str, Depends(oauth2_scheme)], body: CommandBody) -> dict:
    print("token ", token)
    print("BODY ", body)
    commandName = body.header.command
    params = body.params
    print(f"commandName={commandName}")
#   print(f"params={params}")
    result = {
        "resultCode": "OK",
        "resultMessage": f"{commandName} was sent successfull!",
        "resultTime": ""
    }
    match commandName:
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
