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

class Event:
    def __init__(self, eventDict : dict):
        self.eventname : str|None = eventDict.get('eventname')
        self.properties: dict|None = eventDict.get('properties')
        self.result:dict = eventDict.get('result')

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