from TransLink import TransLinkDevice


def testauthorizesales():
    amount = int(input('Enter amount of Authorize sales'))
    print(amount)


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
                testauthorizesales()

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
        print('5. AUTHORIZE')

        print('9. Close POS')
        print('0. Exit')

        nextStep = int(input('Enter next step:'))

        match nextStep:
            case 1:
                result = device.openpos()
                print(result)
            case 2:
                result = device.getsoftwareversions()
                print(result)
            case 3:
                result = device.command_GETPOSSTATUS()
                print(result)
            case 4:
                transport = device.gettransport()
                result = transport.GetSettings()
                print(result)
            case 5:
                result = device.command_AUTHORIZE(amount=1, currencyCode="981", documentNr='4445547844')
                print(result)

            case 9:
                result = device.closepos()
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
            case 1:
                DeviceMenu()
            case 2:
                OperationMenu()
            case 0:
                print('Good luck!')
                break


if __name__ == '__main__':
    MainMenu()
