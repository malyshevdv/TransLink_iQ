
class Settings:
    terminalURL: str = ""
    terminalAlias: str = ""

    apiVersion :str = "v107"
    licenseToken: str = "e034d5a6cf3212826c57f35cffb103905afe5936/f86419d06688b6336ddfe68dc00c214b9b83fb10"

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
        self.terminalAlias = settingsDict.get('terminalAlias')
        self.currencyCode = settingsDict.get('currencyCode')

        # for key, value in settingsDict:
        #     if key in self.__getattribute__():
        #         self[key]

    def SaveSettings(self):
        ...

    

    def SetDefaultSettings(self):
        newSettings = {
           'terminalURL' : 'http://localhost:6679',
           'terminalAlias': 'TerminalBank',
           'currencyCode' : '981'
        }
        self.LoadSettings(newSettings)
