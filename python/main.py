from requests import request

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#ff

class TransLinkDevice:
    _accessToken = ""
    _settings : dict = {}

    def __init__(self):
        pass

    def GetSoftwareVersions(self):
        pass

    def OpenPos(self):

        pass

    def ClosePos(self):
        pass



class POS_Transport():

    def SendCommandToPOS(self, dict : dict):
        responce = request('POST', url='')














# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
