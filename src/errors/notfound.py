from .base import BaseError


class NotFoundError(BaseError):
    ...


class GuildNotFoundError(NotFoundError):
    ...


class CategoryNotFoundError(NotFoundError):
    ...
