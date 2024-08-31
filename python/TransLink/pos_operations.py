from random import randint
from .pos_terminal import POS_terminal

class PosOperation:
    def __init__(self, pos : POS_terminal, documentNr: str = ""):
        self.documentNr = documentNr
        if documentNr == "":
            self.documentNr = self.GetNewdocumentNr()
        self.result = False
        self.receiptText: str = ''
        self.eventList: list = []
        self.errorText : str = ""

    def SetPOS(self, pos : POS_terminal):
        self.pos: POS_terminal = pos
    def GetNewdocumentNr(self):
        return str(randint(10000,99000)) + str(randint(10000,99000))
