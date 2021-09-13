from .base import BaseError

__all__ = (
    "AllianceNotFoundError",
    "CategoryNotFoundError",
    "CityNotFoundError",
    "ColorNotFoundError",
    "DocumentNotFoundError",
    "EmbassyConfigNotFoundError",
    "EmbassyNotFoundError",
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


class ColorNotFoundError(NotFoundError):
    ...


class DocumentNotFoundError(NotFoundError):
    ...


class EmbassyConfigNotFoundError(NotFoundError):
    ...


class EmbassyNotFoundError(NotFoundError):
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
