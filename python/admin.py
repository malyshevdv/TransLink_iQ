from TransLink import TransLinkDevice, PaymentOperationType, Currencies, SupportedLanguages
from pprint import pprint

def testauthorizesales():
    amount = int(input('Enter amount of Authorize sales'))
    pprint(amount)


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

        print('1. Open POS                  2. Show driver version')
        print('3. Get POS status            4. Show settings')
        print('5. GET EVENT                 6. UNLOCK 5')
        print('7. AUTHORIZE                 8. CLOSEDOC')
        print('9. PRINTTOTALS               10. LOCK')
        print('11. Close POS')
        print('0. Exit')
        print('==============')

        nextStep = int(input('Enter next step:'))

        match nextStep:
            case 1:
                result = device.openpos()
                pprint(result)
            case 2:
                result = device.getsoftwareversions()
                pprint(result)
            case 3:
                result = device.command_GETPOSSTATUS()
                pprint(result)
            case 4:
                transport = device.gettransport()
                result = transport.GetSettings()
                pprint(result)
            case 5:
                result = device.getevent()
                pprint(result)

            case 6:
                result = device.unlockdevice(
                    opsOperation = PaymentOperationType.AUTHORIZE,
                    amount = 100,
                    currencyCode = Currencies.GEL,
                    cashBackAmount = 0,
                    language = SupportedLanguages.English,
                    ecrVersion = "001-001-001"
                )
                pprint(result)

            case 7:
                result = device.command_AUTHORIZE(amount=1, currencyCode="981", documentNr='4445547844')
                pprint(result)

            case 9:
                result = device.command_PRINTTOTALS(operatorId="001", operatorName="Denis")
                pprint(result)

            case 10:
                result = device.command_CLOSEDAY(operatorId="001", operatorName="Denis")
                pprint(result)

            case 11:
                result = device.lockdevice()
                pprint(result)

            case 12:
                result = device.closepos()
                pprint(result)
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
