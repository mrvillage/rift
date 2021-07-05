from .base import BaseError


class MessageError(BaseError):
    pass


class LoginError(MessageError):
    pass


class SentError(MessageError):
    pass
