class PsDeliveryException(Exception):
    pass


class RequestTimeout(PsDeliveryException):
    pass


class ElementNotFoundError(PsDeliveryException):
    pass


class WebdriverIsNotLoaded(PsDeliveryException):
    pass
