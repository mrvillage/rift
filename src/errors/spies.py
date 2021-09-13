from .base import BaseError

__all__ = (
    "InvalidSpyResponseError",
    "InvalidReferenceSpyRequestError",
    "SpiesNotFoundError",
)


class BaseSpiesError(BaseError):
    pass


class InvalidSpyResponseError(BaseError):
    pass


class InvalidReferenceSpyRequestError(BaseSpiesError):
    pass


class SpiesNotFoundError(BaseSpiesError):
    pass
