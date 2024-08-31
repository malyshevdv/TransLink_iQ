from .translinkdevice import TransLinkDevice
from .types import PaymentOperationType
from .settings import Settings
import timeit
import time
from .pos_operations import PosOperation


class POS_terminal:

    def __init__(self):
        self.eventList: list = []
        self.pos = TransLinkDevice()

        self._settings = Settings()
        self._settings.SetDefaultSettings()

    def ClearEventList(self):
        self.eventList.clear()

    def GetEventListSize(self):
        return len(self.eventList)

    def GetAllEvents(self):
        self.ClearEventList()
        breackIfEmpty = False
        times = 10


        while True:
            times -=1

            time.sleep(1)
            event = self.pos.GetEvent()
            if not event.Is_EmptyQueue():
                self.eventList.append(event)
                continue

            if  breackIfEmpty and event.Is_EmptyQueue():
                break

            if not breackIfEmpty and \
                    event.InBasicEvents() and \
                    self.GetEventListSize() > 0:
                breackIfEmpty = True

    def HandleAllEvents(self):
        for event in self.eventList:
            if event.eventname == "":
                ...


    def PrintTotals(self):

        posOperation = PosOperation()

        if self.pos.OpenPos():
            typeResult = self.pos.Command_PRINTTOTALS()

            self.GetAllEvents()
            self.HandleAllEvents(posOperation)

        return posOperation


    def AuthorizeSales(self, amount : int, documentNr : str = ""):
        '''make AuthorizeSales operation'''

        posOperation = PosOperation()

        if self.pos.OpenPos():

            props = {'amount' : amount*100,
                     'idleText' : 'Be ready!',
                     'language' : self._settings.language,
                     'ecrVersion' : 'denis-malyshev-001',
                     'currencyCode': self._settings.currencyCode
                    }

            self.pos.UnlockDevice(PaymentOperationType.AUTHORIZE, **props)
            self.GetAllEvents()
            self.HandleAllEvents()

            props = {'amount': amount*100,
                     'currencyCode': self._settings.currencyCode,
                     'documentNr': self.GetNewdocumentNr(),
                     'cashBackAmount': 0
                     }
            self.pos.Command_AUTHORIZE(**props)
            self.GetAllEvents()
            self.HandleAllEvents()

            self.pos.LockDevice()

        return posOperation

