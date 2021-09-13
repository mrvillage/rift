from .base import BaseError

__all__ = ("NoBankPermsError", "NoSendBankPermsError", "NoViewBankPermsError")


class BasePermsError(BaseError):
    ...


class BaseBankPermsError(BasePermsError):
    ...


class NoBankPermsError(BaseBankPermsError):
    ...


class NoSendBankPermsError(NoBankPermsError):
    ...


class NoViewBankPermsError(NoBankPermsError):
    ...
