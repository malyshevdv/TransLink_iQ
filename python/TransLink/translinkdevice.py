from .settings import Settings
from .transport import POS_Transport

class TransLinkDevice:
    _accessToken = ""
    _settings : Settings
    _posTransport : POS_Transport

    def __init__(self):
        self._settings = Settings()
        self._settings.SetDefaultSettings()
        self._posTransport = POS_Transport(self._settings)

    def GetSoftwareVersions(self):
        result = self._posTransport.SendToPOS_(self._settings,)
        return result

    def OpenPos(self):
        result = self._posTransport.SendToPOS('openpos')
        return result


    def ClosePos(self):
        result = self._posTransport.SendToPOS('closepos')
        return result

    def UnlockDevice(self):
        ...
















