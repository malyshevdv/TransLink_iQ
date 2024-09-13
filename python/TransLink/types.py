from typing import Any
from datetime import datetime

def getCurrenDate():
    res = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    print(res)
    return res


class VersionType:
    compatibleApiVersions: list = ""
    releaseVersion = ""


class ResultType:
    resultCode: str = ""
    resultMessage: str = ""
    resultTime: str = ""

    def __init__(self, responceDict : dict):
        self.resultCode:str     = responceDict.get('resultCode','')
        self.resultMessage: str  = responceDict.get('resultMessage','')
        #self.resultTime:str     = responceDict.get('resultTime','')
        #if self.resultTime == "":
        self.resultTime = getCurrenDate()


    def Is_OK(self):
        return self.resultCode == ResultTypeCodes.OK

    def getDict(self):
        return {
            "resultCode": self.resultCode,
            "resultMessage": self.resultMessage,
            "resultTime": self.resultTime
        }

    def __repr__(self):
        return self.getDict()


    def __str__(self):
        return str(self.getDict())

    def GetStatusDescription(self):
        return 'my description'

class ResultTypeCodes:

    OK              : str = 'OK'
    INVALID_ARG     : str = 'INVALID_ARG'
    CONNECTION_ERROR: str = 'CONNECTION_ERROR'
    TIMEOUT         : str = 'TIMEOUT'
    ANOTHER_OPERATION_IN_PROGRESS : str = 'ANOTHER_OPERATION_IN_PROGRESS'
    DECLINED        : str = 'DECLINED'
    NOT_INITILIAZED : str = 'NOT_INITILIAZED'

    @classmethod
    def GetDescription(cls, typeResultCode):

        result = ''

        match typeResultCode:
            case cls.OK:
                result =  'Operation completed successfully.'
            case cls.INVALID_ARG:
                result =  'One of the arguments is invalid. (For example: DocumentNr is null or empty).'
            case cls.CONNECTION_ERROR:
                result =  'No connection to Ashburn POS device or some other connection problem.'
            case cls.TIMEOUT:
                result =  'Timeout waiting for operation to complete.'
            case cls.ANOTHER_OPERATION_IN_PROGRESS:
                result =  'The previous session has not been closed yet.'
            case cls.DECLINED:
                result =  'Operation was declined.'
            case cls.NOT_INITILIAZED:
                result =  'openpos method was not called.'

        return result

class TypeAmountAdditional:
    type: str = ""
    currencyCode: str = ""
    amount : int = 0

class PaymentOperationType:
    NOOPERATION : str = 'NOOPERATION'
    AUTHORIZE   : str = 'AUTHORIZE'
    PREAUTHORIZE: str = 'PREAUTHORIZE'
    CREDIT      : str = 'CREDIT'
    INQUIRY     : str = 'INQUIRY'
    CARDREAD    : str = 'CARDREAD'
    MANUALENTRY : str = 'MANUALENTRY'

class AuthorizationState:
    Notfound    : str = 'Notfound'
    Authorizing : str = 'Authorizing'
    Approved    : str = 'Approved'
    Declined    : str = 'Declined'
    Timeout     : str = 'Timeout'
    Reversing   : str = 'Reversing'
    Reversed    : str = 'Reversed'
    Voiding     : str = 'Voiding'

class TransactionState:
    Approved    : str = 'Approved'
    Declined    : str = 'Declined'



class SupportedLanguages:
    English     = 'EN'
    Lithuanian  = 'LT'
    Russian     = 'RU'
    Latvian     = 'LV'
    Estonian    = 'EE'
    Turkmen     = 'TM'
    Tajik       = 'TJ'
    Georgian    = 'GE'
    Kazakh      = 'KZ'
    Azerbaijani = 'AZ'
    Uzbek       = 'UZ'

class Currencies:
    GEL = "981"
    USD = "840"
    EUR = "978"
    TMT = "934"
    TJS = "972"
    KZT = "398"
    AZN = "944"
    UZS = "860"

    BNS = "111" #BONUS1
    PLS = "211" #BONUS2


class RequestParameters:
    command : str = ''
    params : dict = {}

    def __init__(self, command : str):
        self.command = command
    def Append(self, key: str, value : Any):
        self.params[key] = value

    def GetBody(self):
        result = {
            'header' : {'command' : self.command},
            'params' : self.params.copy()
        }
        return result












