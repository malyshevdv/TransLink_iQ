from .settings import Settings
from .transport import POS_Transport
from .types import RequestParameters, PaymentOperationType


class TransLinkDevice:
    _accessToken = ""
    _settings : Settings
    _posTransport : POS_Transport

    def __init__(self):
        self._settings = Settings()
        self._settings.SetDefaultSettings()
        self._posTransport = POS_Transport(self._settings)

    def GetSoftwareVersions(self):
        '''The method gets the information about the API software. '''

        result = self._posTransport.SendToPOS("getsoftwareversions", method='GET')
        return result

    def OpenPos(self):
        '''The method is designed to trigger connection to the POS device. Together with closepos
        should be used for each EFT operation. '''

        bodyDict = {
            "licenseToken": self._settings.licenseToken,
            "alias": self._settings.terminalAlias,
            "username": "",
            "password": ""
        }
        result = self._posTransport.SendToPOS("openpos", body=bodyDict)
        return result


    def ClosePos(self):
        '''The method is designed to terminate connection to the POS device. '''

        result = self._posTransport.SendToPOS("closepos")
        return result

    def UnlockDevice(self):

        result = self.ExecuteComand(requestParameters.GetBody())
        return result  # TypeResult

def Command_GETPOSSTATUS(self
                    ) -> dict:
    '''4.5.29 GETPOSSTATUS
The command requests the status of the POS. '''

    requestParameters = RequestParameters("GETPOSSTATUS")

    result = self.ExecuteComand(requestParameters.GetBody())
    return result  # TypeResult

def Command_CLOSEDOC(self,
                     documentNr: str,
                     operations: list | None = None,
                     eProducts: list | None = None,
                     fiscalOperations: list | None = None
                     ) -> dict:
    '''4.5.30 CLOSEDOC
Each transaction initiated from the ECR must be confirmed by calling this method. When this method is called, the POS can trigger the
formation of additional receipts, for the receipt of which the ONPRINT event will be generated. When the ECR decides to confirm the
transaction, it must stand by its decision and repeatedly send CLOSEDOC until acknowledgment is received. When a documentNr is sent
without list of operations, every known operation (from the POS terminal perspective) of this document will be reversed (if it was not
confirmed beforehand).'''

    requestParameters = RequestParameters("CLOSEDOC")
    requestParameters.Append("documentNr", documentNr)
    if operations is not None:
        requestParameters.Append("operations", operations)
    if eProducts is not None:
        requestParameters.Append("eProducts", eProducts)
    if fiscalOperations is not None:
        requestParameters.Append("fiscalOperations", fiscalOperations)

    result = self.ExecuteComand(requestParameters.GetBody())
    return result  # TypeResult


def Command_CLOSEEPRODUCT(self,
                     operations: list | None = None,
                     ) -> dict:
    '''4.5.31 CLOSEEPRODUCT* - not in use in the current version
Each operation triggered from the ECR must be confirmed by calling this method. When this method is called,
the POS can trigger the formation of additional register receipts, for the receipt of which the ONPRINT event
will be generated.'''

    requestParameters = RequestParameters("CLOSEEPRODUCT")
    requestParameters.Append("operations", operations)

    result = self.ExecuteComand(requestParameters.GetBody())
    return result  # TypeResult


def Command_CREDIT(self,
                     amount: int,
                     currencyCode: str,
                     documentNr: str,
                     panL4Digit: str | None = None,
                     time: str | None = None,
                     STAN: str | None = None,
                     RRN: str | None = None
                     ) -> dict:
    '''4.5.32 CREDIT
The command triggers in the POS a procedure for refunding to card accounts. '''

    requestParameters = RequestParameters('CREDIT')
    requestParameters.Append("amount", amount)
    requestParameters.Append("currencyCode", currencyCode)
    requestParameters.Append("documentNr", documentNr)
    if panL4Digit is not None:
        requestParameters.Append("panL4Digit", panL4Digit)
    if time is not None:
        requestParameters.Append("time", time)
    if STAN is not None:
        requestParameters.Append("STAN", STAN)
    if RRN is not None:
        requestParameters.Append("RRN", RRN)

    result = self.ExecuteComand(requestParameters.GetBody())
    return result  # TypeResult


def GetEvent(self,
             ) -> dict:
    '''4.6.1 getEvent
The method checks the queue of available events triggered by the API. If pending events are available in the queue, the method will
return the name of the event and the attributes required for processing the event as a result.
It is possible to instruct the server to wait for event if the queue is empty with a technique called HTTP Long Polling.
getEvent?longPollingTimeout=15 would tell the server to wait for 15 seconds (max 60s). '''

    result = self._posTransport.SendToPOS("getsoftwareversions", method='GET')
    return result #EventType


