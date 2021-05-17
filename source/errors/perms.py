from .base import BaseError


class BasePermsError(BaseError):
    pass


class BaseBankPermsError(BasePermsError):
    pass


class NoBankPermsError(BaseBankPermsError):
    pass


class NoSendBankPermsError(NoBankPermsError):
    pass


class NoViewBankPermsError(NoBankPermsError):
    pass
