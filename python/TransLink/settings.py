
class Settings:
    terminalURL: str = ""
    terminalAlias: str = ""

    apiVersion :str = "v107"
    cardTech : list = []
    transactionSourceMedia : list = []

    silentCardRead : bool = True
    language : str = "EN"
    currencyCode : str = ""

    debug : bool = False
    voiceAssistance: bool = False

    loging : bool = True
    logPath : str = ''

    def __init__(self):
        ...


    def LoadSettings(self, settingsDict : dict):
        self.terminalURL  = settingsDict.get('terminalURL')
        self.terminaAlias = settingsDict.get('terminaAlias')
        self.currencyCode = settingsDict.get('currencyCode')

        # for key, value in settingsDict:
        #     if key in self.__getattribute__():
        #         self[key]

    def SaveSettings(self):
        ...

    

    def SetDefaultSettings(self):
        newSettings = {
           'terminalURL' : 'localhost:1987',
           'terminaAlias': 'TerminalBank',
           'currencyCode' : '981'
        }
        self.LoadSettings(newSettings)
