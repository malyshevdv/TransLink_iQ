from typing import Any

class VersionType:
    compatibleApiVersions: list = ""
    releaseVersion = ""


class ResultType:
    resultCode: str = ""
    resultMessage: str = ""
    resultTime: str = ""

    def __init__(self, responceDict : dict):
        self.resultCode     = responceDict.get('resultCode','')
        self.resultMessage  = responceDict.get('resultMessage','')
        self.resultTime     = responceDict.get('resultTime','')

    def Is_OK(self):
        return self.resultCode == TypeResultCodes.OK

    def GetStatusDescription(self):
        ...

class TypeResultCodes:

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


class EventsType:
    ONPROMPT = 'ONPROMPT'
    ONSELECT = 'ONSELECT'
    ONMSGBOX = 'ONMSGBOX'
    ONDISPLAYPROMPTRESULT = 'ONDISPLAYPROMPTRESULT'
    ONDISPLAYMSGBOXRESULT = 'ONDISPLAYMSGBOXRESULT'
    ONDISPLAYSELECTRESULT = 'ONDISPLAYSELECTRESULT'
    ONTRNSTATUS = 'ONTRNSTATUS'
    ONFISCALIZERESULT = 'ONFISCALIZERESULT'
    ONCARD = 'ONCARD'
    ONCARDREMOVE = 'ONCARDREMOVE'
    ONWRITECARDRESULT = 'ONWRITECARDRESULT'
    ONDISPLAYTEXT = 'ONDISPLAYTEXT'
    ONPRINT = 'ONPRINT'
    ONKBD = 'ONKBD'
    ONEPRODUCTRESULT = 'ONEPRODUCTRESULT'









