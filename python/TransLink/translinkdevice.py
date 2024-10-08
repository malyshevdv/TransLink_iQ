from .settings import Settings
from .transport import POS_Transport
from .types import RequestParameters, PaymentOperationType
from .events import Event


class TransLinkDevice:
    """my object"""

    def __init__(self):

        settings = Settings()
        settings.SetDefaultSettings()

        self._posTransport = POS_Transport(settings)

    def gettransport(self):
        return self._posTransport

    def getsoftwareversions(self):
        """The method gets the information about the API software."""

        result = self._posTransport.SendToPOS("getsoftwareversions", method='GET')
        return result


    def isopened(self):
        return self._accessToken != ""

    def openpos(self) -> bool:
        """The method is designed to trigger connection to the POS device. Together with closepos
        should be used for each EFT operation. """

        result = False

        bodyDict = {
                    "licenseToken": self._posTransport._settings.licenseToken,
                    "alias": self._posTransport._settings.terminalAlias,
                    "username": "",
                    "password": ""
                    }
        resultOpenPos = self._posTransport.SendToPOS("openpos", body=bodyDict)
        self._posTransport._accessToken = resultOpenPos.get("json").get('accessToken', "")

        if self._posTransport._accessToken != "":
            result = True

        return result

    def closepos(self):
        """The method is designed to terminate connection to the POS device. """

        result = self._posTransport.SendToPOS("closepos")
        return result

    def executecomand(self, bodyDict: dict) -> dict:
        """4.5 executeposcmd
        The method is designed to transmit a command to the POS device. """

        result = self._posTransport.SendToPOS("executeposcmd", body=bodyDict)
        return result

    def unlockdevice(self,
                     opsOperation: PaymentOperationType,
                     amount: int,
                     idleText: str,
                     language: str,
                     ecrVersion: str,
                     cashBackAmount: int | None = None,
                     currencyCode: str | None = None
                     ):
        """4.5.1 UNLOCKDEVICE
        The command unlocks the POS to execute subsequent operations.
        This command must be executed before starting any calculation
        operation triggered from the ECR.
        :type cashBackAmount: object"""

        requestParameters = RequestParameters("UNLOCKDEVICE")
        requestParameters.Append("opsOperation", opsOperation)
        requestParameters.Append("amount", amount)
        requestParameters.Append("idleText", idleText)
        requestParameters.Append("language", language)
        requestParameters.Append("ecrVersion", ecrVersion)
        if cashBackAmount is not None:
            requestParameters.Append("cashBackAmount", cashBackAmount)
        if currencyCode is not None:
            requestParameters.Append("currencyCode", currencyCode)

        result = self.executecomand(requestParameters.GetBody())
        return result

    def lockdevice(self,
                   idleText: str):
        """4.5.2 LOCKDEVICE
        The command executes POS locking, with the option to display on the screen the message transmitted
        in the idleText parameter. Recommended to be sent after every completed EFT operation. """

        requestParameters = RequestParameters("LOCKDEVICE")
        requestParameters.Append("idleText", idleText)

        result = self.executecomand(requestParameters.GetBody())
        return result


    def getevent(self,
                 ) -> Event:
        """4.6.1 getEvent
    The method checks the queue of available events triggered by the API. If pending events are available
    in the queue, the method will return the name of the event and the attributes required for processing the event
    as a result.
    It is possible to instruct the server to wait for event if the queue is empty with a technique called HTTP
     Long Polling.  getEvent?longPollingTimeout=15 would tell the server to wait for 15 seconds (max 60s). """

        result = self._posTransport.SendToPOS("getevent", method='GET')
        event = Event(result)
        return event



    def command_AUTHORIZE(self,
                          amount: int,
                          currencyCode: str,
                          documentNr: str,
                          cashBackAmount: int = 0,
                          panL4Digit: str | None = None,
                          ecrData: str | None = None
                          ) -> dict:
        """4.5.3 AUTHORIZE
        The command triggers the authorization procedure (payment for purchases) on the POS. """

        requestParameters = RequestParameters('AUTHORIZE')
        requestParameters.Append("amount", amount)
        requestParameters.Append("currencyCode", currencyCode)
        requestParameters.Append("documentNr", documentNr)
        requestParameters.Append("cashBackAmount", cashBackAmount)
        if panL4Digit is not None:
            requestParameters.Append("panL4Digit", panL4Digit)
        if ecrData is not None:
            requestParameters.Append("ecrData", ecrData)

        result = self.executecomand(requestParameters.GetBody())
        return result

    def command_PREAUTHORIZE(self,
                             amount: int,
                             currencyCode: str,
                             documentNr: str,
                             panL4Digit: str | None = None,
                             ecrData: str | None = None
                             ) -> dict:
        """4.5.4 PREAUTHORIZE
        The command triggers a pre-authorization request on the POS.  The method can be called after receiving
        the ONCARD event and in the case when allowPreAuthorize – the flag of permission for the pre-authorization
        operation is set . """

        requestParameters = RequestParameters("PREAUTHORIZE")
        requestParameters.Append("amount", amount)
        requestParameters.Append("currencyCode", currencyCode)
        requestParameters.Append("documentNr", documentNr)
        if panL4Digit is not None:
            requestParameters.Append("panL4Digit", panL4Digit)
        if ecrData is not None:
            requestParameters.Append("ecrData", ecrData)

        result = self.executecomand(requestParameters.GetBody())
        return result

    def command_INCREMENT(self,
                          amount: int,
                          operationId: str,
                          cryptogram: str | None = None
                          ) -> dict:
        """4.5.5 INCREMENT
        The command triggers the POS request to increase the amount of previously confirmed pre-authorization."""

        requestParameters = RequestParameters("PREAUTHORIZE")
        requestParameters.Append("amount", amount)
        requestParameters.Append("operationId", operationId)
        if cryptogram is not None:
            requestParameters.Append("cryptogram", cryptogram)

        result = self.executecomand(requestParameters.GetBody())
        return result

    def command_COMPLETE(self,
                         amount: int,
                         operationId: str,
                         cryptogram: str | None = None,
                         noShow: bool | None = None
                         ) -> dict:
        """4.5.6 COMPLETE

        The command triggers a request for confirmation in the POS of a previously performed preauthorization operation.

        After completing preauthorization with the Complete command, re-calling the Increment or Complete commands is
        not allowed. Gettrnstatus can be used to check the preauthorization status. If preauthorization is completed,
        the state attribute  will have the Settled value. To cancel the completed preauthorization, the Void method
        must be used. To cancel (terminate) incomplete pre-authorization, Complete with a zero amount must be used."""

        requestParameters = RequestParameters("COMPLETE")
        requestParameters.Append("amount", amount)
        requestParameters.Append("operationId", operationId)

        if cryptogram is not None:
            requestParameters.Append("cryptogram", cryptogram)
        if noShow is not None:
            requestParameters.Append("noShow", noShow)

        result = self.executecomand(requestParameters.GetBody())

        return result

    def command_INSTALLMENT(self,
                            amount: int,
                            installmentPaymentCount: int,
                            documentNr: str,
                            installmenProvider: str | None = None,
                            currencyCode: str | None = None,
                            panL4Digit: str | None = None,
                            ecrData: str | None = None
                            ) -> dict:
        """4.5.7 INSTALLMENT
The command triggers the consumer credit procedure for the payment transaction in progress. To prepare the terminal
for this operation, UNLOCKDEVICE with Operation code 0 (NOOPERATION) with sum 0 must be sent."""

        Parameters = RequestParameters("INSTALLMENT")
        Parameters.Append("amount", amount)
        Parameters.Append("installmentPaymentCount", installmentPaymentCount)
        Parameters.Append("documentNr", documentNr)

        if installmenProvider is not None:
            Parameters.Append("installmenProvider", installmenProvider)
        if currencyCode is not None:
            Parameters.Append("currencyCode", currencyCode)
        if panL4Digit is not None:
            Parameters.Append("panL4Digit", panL4Digit)
        if ecrData is not None:
            Parameters.Append("ecrData", ecrData)

        result = self.executecomand(Parameters.GetBody())
        return result  # TypeResult

    def command_CREDIT(self,
                       amount: int,
                       currencyCode: str,
                       documentNr: str,
                       panL4Digit: str | None = None,
                       time: str | None = None,
                       STAN: str | None = None,
                       RRN: str | None = None,
                       ecrData: str | None = None
                       ) -> dict:
        """4.5.8 CREDIT
The command triggers in the POS a procedure for refunding to card accounts. """

        requestParameters = RequestParameters('CREDIT')
        requestParameters.Append("amount", amount)
        requestParameters.Append("currencyCode", currencyCode)
        requestParameters.Append("documentNr", documentNr)

        if panL4Digit is not None:
            requestParameters.Append("panL4Digit", panL4Digit)
        if time is not None:
            requestParameters.Append("time", time)
        if STAN is not None:
            requestParameters.Append("STAN", STAN)
        if RRN is not None:
            requestParameters.Append("RRN", RRN)
        if ecrData is not None:
            requestParameters.Append("ecrData", ecrData)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_VOID(self,
                     operationId: str,
                     ) -> dict:
        """4.5.9 VOID
    Cancellation/termination of the previously authorized card transaction.
    This operation is allowed during a banking day."""

        requestParameters = RequestParameters('VOID')
        requestParameters.Append('operationId', operationId)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_VOIDPARTIAL(self,
                            operationId: str,
                            voidAmount: str,
                            originalAmount: str
                            ) -> dict:
        """4.5.10 VOIDPARTIAL
    Partial cancellation of the previously authorized card transaction."""

        parameters = RequestParameters("VOIDPARTIAL")
        parameters.Append("operationId", operationId)
        parameters.Append("voidAmount", voidAmount)
        parameters.Append("originalAmount", originalAmount)

        result = self.executecomand(parameters.GetBody())
        return result  # TypeResult

    def command_FISCALIZE(self,
                          documentNr: str,
                          type: str,
                          items: list | None = None,
                          exciseId: str | None = None
                          ) -> dict:
        """4.5.11 FISCALIZE
    The command starts fiscalization of payment. """

        requestParameters = RequestParameters("FISCALIZE")
        requestParameters.Append("documentNr", documentNr)
        requestParameters.Append("type", type)
        if items is not None:
            requestParameters.Append("items", items)
        if exciseId is not None:
            requestParameters.Append("exciseId", exciseId)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_GETFISCALIZESTATE(self,
                                  documentNr: str,
                                  ) -> dict:
        """4.5.12 GETFISCALIZESTATE
    Get information about fiscal operation if you do not have response to the original FISCALIZE request. """

        requestParameters = RequestParameters("GETFISCALIZESTATE")
        requestParameters.Append("documentNr", documentNr)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_PRINT(self,
                      receiptText: str,
                      documentNr: str | None = None
                      ) -> dict:
        """4.5.13 PRINT
    The command prints the register receipt on the integrated POS printer."""

        requestParameters = RequestParameters("PRINT")
        requestParameters.Append("receiptText", receiptText)
        if documentNr is not None:
            requestParameters.Append("documentNr", documentNr)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_DISPLAYMEDIA(self,
                             displayText: str,
                             imageId: str | None = None
                             ) -> dict:
        """4.5.14 DISPLAYMEDIA
    The command requests the terminal to display a message and optionally an image."""

        requestParameters = RequestParameters("DISPLAYMEDIA")
        requestParameters.Append("displayText", displayText)
        if imageId is not None:
            requestParameters.Append("imageId", imageId)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_DISPLAYPROMPT(self,
                              displayText: str,
                              inputMask: str
                              ) -> dict:
        """4.5.15 DISPLAYPROMPT
    The command requests the terminal to display a message to enter requested information. Result is received with a
    ONDISPLAYPROMPTRESULT event. """

        requestParameters = RequestParameters("DISPLAYPROMPT")
        requestParameters.Append("displayText", displayText)
        requestParameters.Append("inputMask", inputMask)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_DISPLAYMSGBOX(self,
                              displayText: str,
                              boxButtons: str
                              ) -> dict:
        """4.5.16 DISPLAYMSGBOX
    The command requests the terminal to display a message with action to be taken (a button pressed). Result
    is received with a ONDISPLAYMSGBOXRESULT event. """

        requestParameters = RequestParameters("DISPLAYMSGBOX")
        requestParameters.Append("displayText", displayText)
        requestParameters.Append("boxButtons", boxButtons)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_DISPLAYSELECT(self,
                              displayText: str,
                              options: list
                              ) -> dict:
        """4.5.17 DISPLAYSELECT
    The command requests the terminal to display a message with a list of options.
    Result is received with a ONDISPLAYSELECTRESULT event. """

        requestParameters = RequestParameters("DISPLAYSELECT")
        requestParameters.Append("displayText", displayText)
        requestParameters.Append("options", options)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_SETPROMPTINPUT(self,
                               inputValue: str
                               ) -> dict:
        """4.5.18 SETPROMPTINPUT
    The command is designed to transmit input information according to the ONPROMPT event."""

        requestParameters = RequestParameters("SETPROMPTINPUT")
        requestParameters.Append("inputValue", inputValue)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_SETMSGBOXKEY(self,
                             keyValue: str
                             ) -> dict:
        """4.5.19 SETMSGBOXKEY
    The command is designed to transmit input information according to the ONMSGBOX event. """

        requestParameters = RequestParameters("SETMSGBOXKEY")
        requestParameters.Append("keyValue", keyValue)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_SETSELECTEDVALUE(self,
                                 selectedValue: str
                                 ) -> dict:
        """4.5.20 SETSELECTEDVALUE
    The command is designed to transmit input information according to the ONSELECT event. """

        requestParameters = RequestParameters("SETSELECTEDVALUE")
        requestParameters.Append("selectedValue", selectedValue)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_CLOSEDAY(self,
                         operatorId: str | None = None,
                         operatorName: str | None = None
                         ) -> dict:
        """4.5.21 CLOSEDAY
    The command triggers the “Close Business day” procedure on the POS terminal. """

        requestParameters = RequestParameters("CLOSEDAY")
        if operatorId is not None:
            requestParameters.Append("operatorId", operatorId)
        if operatorName is not None:
            requestParameters.Append("operatorName", operatorName)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_PRINTTOTALS(self,
                            operatorId: str | None = None,
                            operatorName: str | None = None
                            ) -> dict:
        """4.5.22 PRINTTOTALS
    The command triggers the generation of transactions report on the POS. If the terminal has an integrated printer,
    the report will be printed by the POS printer, otherwise the ONPRINT event will be triggered, in which the report
    text will be transmitted."""

        requestParameters = RequestParameters("PRINTTOTALS")
        if operatorId is not None:
            requestParameters.Append("operatorId", operatorId)
        if operatorName is not None:
            requestParameters.Append("operatorName", operatorName)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_GETTRNSTATUS(self,
                             documentNr: str | None = None,
                             operationId: str | None = None,
                             cryptogram: str | None = None
                             ) -> dict:
        """4.5.23 GETTRNSTATUS
    The command makes a request about the status of a preauthorization transaction. Using operationId and cryptogram
    when possible is the preferred method, since it would work for preauthorizations made on different terminals.
    If one of them is lost, documentNr could be used. """

        requestParameters = RequestParameters("GETTRNSTATUS")
        if documentNr is not None:
            requestParameters.Append("documentNr", documentNr)
        elif operationId is not None and cryptogram is not None:
            requestParameters.Append("operationId", operationId)
            requestParameters.Append("cryptogram", cryptogram)
        else:
            ...

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_INQUIRYBALANCE(self
                               ) -> dict:
        """4.5.24 INQUIRYBALANCE
    The command makes a request about the balance of the payment card. The balance
    information is displayed on the POS screen."""

        requestParameters = RequestParameters("INQUIRYBALANCE")

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_EPRODUCTQUERY(self,
                              barcodeData: str,
                              documentNr: str | None = None
                              ) -> dict:
        """4.5.25 EPRODUCTQUERY
    The command triggers a request for payment for the e-product by transmitting
    the payer's identifier or QRCode as a parameter.
    While interpreting the response received from a third party, the POS may request
    for additional data from the ECR operator by sending
    various requests for input and selection of e-product parameters"""

        requestParameters = RequestParameters("EPRODUCTQUERY")
        requestParameters.Append("barcodeData", barcodeData)
        if documentNr is not None:
            requestParameters.Append("documentNr", documentNr)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_WRITECARD(self,
                          dataBlocks: list,
                          UID: str | None = None,
                          silent: str | None = None
                          ) -> dict:
        """4.5.26 WRITECARD
    The command tells the POS to write data to the card using one of the technologies available."""

        requestParameters = RequestParameters("WRITECARD")
        requestParameters.Append("dataBlocks", dataBlocks)
        if UID is not None:
            requestParameters.Append("UID", UID)
        if silent is not None:
            requestParameters.Append("silent", silent)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_REMOVECARD(self,
                           text: str
                           ) -> dict:
        """4.5.27 REMOVECARD
    The command is used to inform the cardholder through the POS device that this card is not processed.
    The command triggers the display of the information message for the cardholder, which indicates the
    reason why the card is not processed."""

        requestParameters = RequestParameters("REMOVECARD")
        requestParameters.Append("text", text)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult
    
    def command_GETPOSSTATUS(self):
        result = self._posTransport.SendCommandToPOS(commandName="GETPOSSTATUS")
        return result

    def command_BEEP(self,
                     notes: list
                     ) -> dict:
        """4.5.28 BEEP
    The command instructs POS terminal to play a sound sequence using device internal beeper."""

        requestParameters = RequestParameters("BEEP")
        requestParameters.Append("notes", notes)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_GETPOSSTATUS(self
                             ) -> dict:
        """4.5.29 GETPOSSTATUS
    The command requests the status of the POS. """

        requestParameters = RequestParameters("GETPOSSTATUS")

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_CLOSEDOC(self,
                         documentNr: str,
                         operations: list | None = None,
                         eProducts: list | None = None,
                         fiscalOperations: list | None = None
                         ) -> dict:
        """4.5.30 CLOSEDOC
    Each transaction initiated from the ECR must be confirmed by calling this method. When this method is
    called, the POS can trigger the  formation of additional receipts, for the receipt of which the ONPRINT
    event will be generated. When the ECR decides to confirm the transaction, it must stand by its decision and
    repeatedly send CLOSEDOC until acknowledgment is received. When a documentNr is sent without list of operations,
    every known operation (from the POS terminal perspective) of this document will be reversed (if it was not
    confirmed beforehand)."""

        requestParameters = RequestParameters("CLOSEDOC")
        requestParameters.Append("documentNr", documentNr)
        if operations is not None:
            requestParameters.Append("operations", operations)
        if eProducts is not None:
            requestParameters.Append("eProducts", eProducts)
        if fiscalOperations is not None:
            requestParameters.Append("fiscalOperations", fiscalOperations)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_CLOSEEPRODUCT(self,
                              operations: list | None = None,
                              ) -> dict:
        """4.5.31 CLOSEEPRODUCT* - not in use in the current version
    Each operation triggered from the ECR must be confirmed by calling this method. When this method is called,
    the POS can trigger the formation of additional register receipts, for the receipt of which the ONPRINT event
    will be generated."""

        requestParameters = RequestParameters("CLOSEEPRODUCT")
        requestParameters.Append("operations", operations)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

    def command_CREDIT(self,
                       amount: int,
                       currencyCode: str,
                       documentNr: str,
                       panL4Digit: str | None = None,
                       time: str | None = None,
                       STAN: str | None = None,
                       RRN: str | None = None
                       ) -> dict:
        """4.5.32 CREDIT
    The command triggers in the POS a procedure for refunding to card accounts. """

        requestParameters = RequestParameters('CREDIT')
        requestParameters.Append("amount", amount)
        requestParameters.Append("currencyCode", currencyCode)
        requestParameters.Append("documentNr", documentNr)
        if panL4Digit is not None:
            requestParameters.Append("panL4Digit", panL4Digit)
        if time is not None:
            requestParameters.Append("time", time)
        if STAN is not None:
            requestParameters.Append("STAN", STAN)
        if RRN is not None:
            requestParameters.Append("RRN", RRN)

        result = self.executecomand(requestParameters.GetBody())
        return result  # TypeResult

