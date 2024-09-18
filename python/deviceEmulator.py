from fastapi import FastAPI, Depends, Request, WebSocket, WebSocketException, Query, Cookie, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Annotated
from pydantic import BaseModel

from PosEmulator import PosEmulator

from pprint import pprint


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

url = "/v107"

posEmulator = PosEmulator("POSS2")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=posEmulator.getAccessToken())



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    '''This is a start page. There is presented POS-emulator form and
    any specific config dates and statuses'''
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
        mydata = posEmulator.getConfig()
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
    """The method is designed to trigger connection to the POS device.
    Together with closepos should be used for each EFT operation.
    """
    return posEmulator.openpos(body.licenseToken)


@app.post(url + "/closepos")
def closepos(accessToken: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """The method is designed to terminate connection to the POS device.
    The result of execution of the TypeResult command.
    """
    print("Authorization ", accessToken)

    return posEmulator.closepos(accessToken)


@app.get(url + "/getsoftwareversions")
def getsoftwareversions(accessToken: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    if accessToken == "":
        print('Empty token')

    return posEmulator.getsoftwareversions()


@app.get(url + "/getevent")
def getevent(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """The method checks the queue of available events triggered by the API. If pending events are available in the
     queue, the method will return the name of the event and the attributes required for processing the event as a
     result.
     It is possible to instruct the server to wait for event if the queue is empty with a technique called HTTP
     Long Polling.
     getEvent?longPollingTimeout=15 would tell the server to wait for 15 seconds (max 60s).
     eventList:
     ONPROMPT
     ONSELECT
     ONMSGBOX
     ONDISPLAYPROMPTRESULT
     ONDISPLAYMSGBOXRESULT
     ONDISPLAYSELECTRESULT
     ONTRNSTATUS
     ONFISCALIZERESULT
     ONCARD
     ONCARDREMOVE
     ONWRITECARDRESULT
     ONDISPLAYTEXT
     ONPRINT
     ONKBD
     ONEPRODUCTRESULT


     """
    if token == "":
        print('Empty token')

    return posEmulator.getEvent()


@app.post(url + "/executeposcmd")
def executeposcmd(token: Annotated[str, Depends(oauth2_scheme)], body: CommandBody) -> dict:
    """The command unlocks the POS to execute subsequent operations. This command must be executed before starting
    any calculation operation triggered from the ECR.
    Command list:
    UNLOCKDEVICE
    LOCKDEVICE
    AUTHORIZE
    PREAUTHORIZE
    INCREMENT
    COMPLETE
    INSTALLMENT
    CREDIT
    VOID
    VOIDPARTIAL
    FISCALIZE
    GETFISCALIZESTATE
    PRINT
    DISPLAYMEDIA
    DISPLAYPROMPT
    DISPLAYMSGBOX
    DISPLAYSELECT
    SETPROMPTINPUT
    SETMSGBOXKEY
    SETSELECTEDVALUE
    CLOSEDAY
    PRINTTOTALS
    GETTRNSTATUS
    INQUIRYBALANCE
    EPRODUCTQUERY
    WRITECARD
    REMOVECARD
    BEEP
    GETPOSSTATUS
    CLOSEDOC
    CLOSEEPRODUCT* - not in use in the current version
    CREDIT



    """

    print("token ", token)
    print("BODY ", body)
    commandname = body.header.command

    return posEmulator.executeposcmd(commandname, body)



