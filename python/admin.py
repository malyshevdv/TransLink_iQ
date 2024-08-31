from TransLink import TransLinkDevice

def Test_AuthorizeSales():
    Amount = int(input('Enter amount of Authorize sales'))


def ShowDriverVersion():
    ...
def OperationMenu():
    while True:
        print('==============')
        print('Operation menu')

        print('1. Authorize Sales')
        print('2. Authorize Void')
        print('3. Authorize Void Partial')

        print('8. Print totals')
        print('9. Close day')
        print('0. Exit')

        nextStep = int(input('Enter next step:'))

        match nextStep:
            case 1:
                Test_AuthorizeSales()

            case 0:
                    break

def DeviceMenu():

    device = TransLinkDevice()

    while True:
        print('==============')
        print('Test device menu')

        print('1. Open POS')
        print('2. Show driver version')
        print('3. Get POS status')
        print('4. Show settings')

        print('9. Close POS')
        print('0. Exit')

        nextStep = int(input('Enter next step:'))

        match nextStep:
            case 1 :
                    result = device.OpenPos()
                    print(result)
            case 2:
                    result = device.GetSoftwareVersions()
                    print(result)
            case 3:
                    result = device.Command_GETPOSSTATUS()
                    print(result)
            case 4:
                result = device._posTransport.GetSettings()
                print(result)

            case 9:
                    result = device.ClosePos()
                    print(result)
            case 0:
                    break

def MainMenu():

    device = TransLinkDevice()

    while True:
        print('==============')
        print('Test device menu')

        print('1. Device test')
        print('2. Operation test')
        print('0. Exit')

        nextStep = int(input('Enter next step:'))

        match nextStep:
            case 1 :
                    DeviceMenu()
            case 2:
                    OperationMenu()
            case 0:
                print('Good luck!')
                break


if __name__ == '__main__':

    MainMenu()

