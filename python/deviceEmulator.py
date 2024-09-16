from fastapi import FastAPI, Depends, Request, WebSocket, WebSocketException, Query, Cookie, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Annotated
from pydantic import BaseModel
from TransLink import Event, Events
from pprint import pprint


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

url = "/v107"
licenseToken = "e034d5a6cf3212826c57f35cffb103905afe5936/f86419d06688b6336ddfe68dc00c214b9b83fb10"

accessToken = "7C65891202494794599402621701736360258001"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=accessToken)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    '''This is a start page'''
    myid = "111222333"
    return templates.TemplateResponse(
        request=request, name="start.html", context={"id": myid}
    )


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/ws")
async def infosocket(*,
                     websocket: WebSocket,
                     #item_id: str,
                     #q: int | None = None,
                     #cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
                     ):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        #await websocket.send_text(f"Message text was: {data}")
        mydata = {"name" : "POS1",
                  "text" : "BE READY",
                  "queue" : "empty",
                  "lasttext" : data
                  }
        await websocket.send_json(mydata)


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
    commandname = body.header.command
    params = body.params
    print(f"commandName={commandname}")
#   print(f"params={params}")
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
