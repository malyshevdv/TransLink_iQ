from TransLink import TransLinkDevice

def ShowDriverVersion():
    ...

def startMenu():

    device = TransLinkDevice()

    while True:
        print('Test device menu')

        print('1. Open POS')
        print('2. Show driver version')
        print('9. Close POS')
        print('0. Exit')

        nextStep = int(input('Enter next step:'))

        match nextStep:
            case 1 :
                    result = device.OpenPos()
                    print(result)
            case 2:
                    result = device.GetDriverVersion()
                    print(result)
            case 9:
                    result = device.ClosePos()
                    print(result)
            case 0:
                    print('Good luck!')
                    break

if __name__ == '__main__':

    startMenu()

