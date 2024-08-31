from typing import Union, Annotated
from fastapi import FastAPI, Header, Body, Request, Depends
from fastapi.security import OAuth2PasswordBearer

import time
from pydantic import BaseModel

class OpenPosBody(BaseModel):
    licenseToken: str = "",
    alias: str = "",
    username: str = "",
    password : str = ""

app = FastAPI()
url = "/v107"
licenseToken = "e034d5a6cf3212826c57f35cffb103905afe5936/f86419d06688b6336ddfe68dc00c214b9b83fb10"

accessToken = "7C65891202494794599402621701736360258001"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=accessToken)

@app.get("/")
def read_root():
    return {"Hello": "TransLink POS amulator - see docs http://127.0.0.1:6678/docs#/"}

@app.post(url + "/openpos")
def openpos(body : OpenPosBody): #Annotated[OpenPosBody, Body()]):
    print("HELLO - ", body)

    if body.licenseToken != licenseToken:
        return UnAuthorizationResult_bedkey()

    result = {
        "accessToken": accessToken
    }
    return result

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.post(url + "/closepos")
def closepos(token: Annotated[str, Depends(oauth2_scheme)]):
    print("Authorization ", token)

    result = {
        "resultCode": "OK",
        "resultMessage": "closepos was sent",
        "resultTime": ""
    }
    return result




def CheckAuth(Authorization : str):
    return accessToken in Authorization
def UnAuthorizationResult():
    result = {
        "resultCode": "NOT_INITILIAZED",
        "resultMessage": "UnAuthorization Result",
        "resultTime": ""
    }
    return result

def UnAuthorizationResult_bedkey():
    result = {
        "resultCode": "NOT_INITILIAZED",
        "resultMessage": "key error",
        "resultTime": ""
    }
    return result
