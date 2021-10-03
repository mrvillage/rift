from .base import BaseError

__all__ = (
    "InvalidSpyResponseError",
    "InvalidReferenceSpyRequestError",
    "SpiesNotFoundError",
)


class BaseSpiesError(BaseError):
    ...


class InvalidSpyResponseError(BaseError):
    ...


class InvalidReferenceSpyRequestError(BaseSpiesError):
    ...


class SpiesNotFoundError(BaseSpiesError):
    ...
