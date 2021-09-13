from .base import BaseError

__all__ = (
    "AllianceNotFoundError",
    "CategoryNotFoundError",
    "CityNotFoundError",
    "DocumentNotFoundError",
    "GuildNotFoundError",
    "MenuItemNotFoundError",
    "MenuNotFoundError",
    "NationNotFoundError",
    "RecipientNotFoundError",
    "ServerNotFoundError",
)


class NotFoundError(BaseError):
    ...


class AllianceNotFoundError(NotFoundError):
    ...


class CategoryNotFoundError(NotFoundError):
    ...


class CityNotFoundError(NotFoundError):
    ...


class DocumentNotFoundError(NotFoundError):
    ...


class GuildNotFoundError(NotFoundError):
    ...


class MenuItemNotFoundError(NotFoundError):
    ...


class MenuNotFoundError(NotFoundError):
    ...


class NationNotFoundError(NotFoundError):
    ...


class RecipientNotFoundError(NotFoundError):
    ...


class ServerNotFoundError(NotFoundError):
    ...
