from .base import BaseError

__all__ = ("NoCredentialsError",)


class CredentialsError(BaseError):
    ...


class NoCredentialsError(CredentialsError):
    ...
