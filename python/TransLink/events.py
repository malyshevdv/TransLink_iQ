from datetime import datetime
from .types import ResultType


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

def getCurrenDate():
    res = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    print(res)
    return res

class Event:
    def __init__(self, eventDict : dict):
        if eventDict.get('status_code') == 200:
            self.eventname : str|None = eventDict.get('eventname')
            self.properties: dict|None = eventDict.get('properties')
            self.result:ResultType|None = ResultType(eventDict.get('result'))
        else:
            self.eventname: str | None = None
            self.properties: dict | None = None
            self.result: ResultType|None = None

    def __str__(self):
        result = {
            "eventname" : self.eventname,
            "properties" : self.properties,
            "result" : self.result
            }
        return str(result)


    def __repr__(self):
        result = {
            "eventname": self.eventname,
            "properties": self.properties,
            "result": self.result
            }
        return result


    def Is_EmptyQueue(self):
        return self.eventname is None and \
            self.result.get('resultCode') == 'OK' and \
            self.result.get('resultMessage') == 'Queue empty.'

    def InBasicEvents(self):
        MyList = [
            EventsType.ONCARD,
            EventsType.ONCARDREMOVE,
            EventsType.ONPRINT,
            EventsType.ONTRNSTATUS
        ]
        return self.eventname in MyList


class Events:
    evetList = []
    @classmethod
    def getEvent(cls):
        result = {
            "eventName": None,
            "properties": None,
            "result": {
                "resultCode": "OK",
                "resultMessage": "Queue empty.",
                "resultTime": getCurrenDate()
                }
            }

        if len(cls.evetList) > 0:
            print(len(cls.evetList))
            print(cls.evetList)
            result = cls.evetList.pop(0)
            print(cls.evetList)

        return result

    @classmethod
    def createevent_ONCARD(cls, body):
        result = {
            "eventName": "ONCARD",
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
                      "resultTime": getCurrenDate()
                      }
            }
        #return result
        cls.evetList.append(result)

    @classmethod
    def createevent_CLOSEDAY_ONPRINT(cls, body):
        result = {
            "eventName": "ONPRINT",
            "properties": {
                "receiptText": " CLOEDAY         End of Day report\n--------------------------------------\n\n\n              TEST BANK\nMerchant: Ashburn International GE\nAddress: Adress str. 17\n\nTerminal ID: 1C000001\n\nSet 1 \"Visa\"                       GEL\nTransactions:    1                1.00\nCancelled:       0                0.00\nTotal:           1                1.00\n\nSet 2 \"Mastercard\"                 GEL\nTransactions:    1                2.00\nCancelled:       0                0.00\nTotal:           1                2.00\n\nTotal                              GEL\nTransactions:    2                3.00\nCancelled:       0                0.00\nTotal:           2                3.00\n______________________________________\nOK                 2024-08-08 13:32:33\n\n",
                "documentNr": ""
            },
            "result": {
                "resultCode": "OK",
                "resultMessage": "Operation completed successfully",
                "resultTime": getCurrenDate()
            }
        }
        cls.evetList.append(result)

    @classmethod
    def createevent_PRINTTOTALS_ONPRINT(cls, body):
        result = {
            "eventName": "ONPRINT",
            "properties": {
                "receiptText": " PRINTTOTALS         End of Day report\n--------------------------------------\n\n\n              TEST BANK\nMerchant: Ashburn International GE\nAddress: Adress str. 17\n\nTerminal ID: 1C000001\n\nSet 1 \"Visa\"                       GEL\nTransactions:    1                1.00\nCancelled:       0                0.00\nTotal:           1                1.00\n\nSet 2 \"Mastercard\"                 GEL\nTransactions:    1                2.00\nCancelled:       0                0.00\nTotal:           1                2.00\n\nTotal                              GEL\nTransactions:    2                3.00\nCancelled:       0                0.00\nTotal:           2                3.00\n______________________________________\nOK                 2024-08-08 13:32:33\n\n",
                "documentNr": ""
            },
            "result": {
                "resultCode": "OK",
                "resultMessage": "Operation completed successfully",
                "resultTime": getCurrenDate()
            }
        }
        cls.evetList.append(result)

    @classmethod
    def createevent_AUTORISE_ONPRINT(cls, body):
        result = {
            "eventName": "ONPRINT",
            "properties": {
                "receiptText": "\\mc\n\\imRANDOM.IMG\n  \n        Ashburn International\n       Tbilisi, Adress str. 17\n       Ashburn International GE\n  \n           ბარათით გადახდა\n                ყიდვა\n  \n              უკონტაქტო\n\nქვითარი:                        100119\nტერმინალი:                    1C000001\nმოვაჭრე:                     1C1000001\nRRN:                      4221RR100119\nთარიღი და დრო:     2024.08.08 11:39:41\nბარათი:               414051******2480\n                                  Visa\n                                     /\nAID:A0000000031010 \n  \nთანხის ოდენობა:               1.00 GEL\n  \nავტორიზაციის კოდი:      79649Z     T:1\n  \n  \n000 OK\n  \n            დადასტურებულია\n\\cl\n\\imRANDOM.IMG\n  \n        Ashburn International\n       Tbilisi, Adress str. 17\n       Ashburn International GE\n  \n           ბარათით გადახდა\n                ყიდვა\n  \n              უკონტაქტო\n\nქვითარი:                        100119\nტერმინალი:                    1C000001\nმოვაჭრე:                     1C1000001\nRRN:                      4221RR100119\nთარიღი და დრო:     2024.08.08 11:39:41\nბარათი:               414051******2480\n                                  Visa\n                                     /\nAID:A0000000031010 \n  \nთანხის ოდენობა:               1.00 GEL\n  \nავტორიზაციის კოდი:      79649Z     T:1\n  \n  \n000 OK\n  \n            დადასტურებულია\n",
                "documentNr": "307855"},
            "result": {
                "resultCode": "OK",
                "resultMessage": "Operation completed successfully",
                "resultTime": getCurrenDate()
            }
        }
        cls.evetList.append(result)

    @classmethod
    def createevent_ONTRNSTATUS(cls, body):
        result = {
            "eventName": "ONTRNSTATUS",
            "properties": {
                "operationId": "OF8B2CFCCBF6E71CB",
                "amountAuthorized": 100,
                "documentNr": "307855",
                "cryptogram": None,
                "authCode": "79649Z",
                "RRN": "4221RR100119",
                "STAN": "119",
                "cardType": "VISA",
                "amountAdditional": None,
                "text": "000 - OK",
                "state": "Approved",
                "authorizationState": "",
                "cardName": "Visa",
                "APN": "Visa Credit",
                "AID": "A0000000031010",
                "CVMApplied": ["NoCVM"],
                "authCenterName": "TEST BANK",
                "tranSourceMedia": "EmvContactless",
                "PAN": "414051******2480",
                "DCCResult": "DccNotOffered",
                "EcrData": ""
            },
            "result": {
                "resultCode": "OK",
                "resultMessage": "Operation completed successfully",
                "resultTime": getCurrenDate()
            }
        }
        cls.evetList.append(result)
