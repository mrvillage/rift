from .base import BaseError


class BankError(BaseError):
    pass


class RecipientNotFoundError(BankError):
    pass
