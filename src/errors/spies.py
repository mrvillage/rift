from .base import BaseError


class BaseSpiesError(BaseError):
    pass


class InvalidSpyResponseError(BaseError):
    pass


class InvalidReferenceSpyRequestError(BaseSpiesError):
    pass


class SpiesNotFoundError(BaseSpiesError):
    pass