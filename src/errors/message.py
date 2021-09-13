from .base import BaseError

__all__ = ("MessageError", "LoginError", "SentError")


class MessageError(BaseError):
    ...


class LoginError(MessageError):
    ...


class SentError(MessageError):
    ...
