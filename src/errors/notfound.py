from .base import BaseError

__all__ = (
    "AllianceNotFoundError",
    "AttackNotFoundError",
    "CategoryNotFoundError",
    "CityNotFoundError",
    "ColorNotFoundError",
    "DocumentNotFoundError",
    "EmbassyConfigNotFoundError",
    "EmbassyNotFoundError",
    "ForumNotFoundError",
    "GuildNotFoundError",
    "MenuItemNotFoundError",
    "MenuNotFoundError",
    "NationNotFoundError",
    "RecipientNotFoundError",
    "ServerNotFoundError",
    "SubscriptionNotFoundError",
    "TargetNotFoundError",
    "TicketConfigNotFoundError",
    "TicketNotFoundError",
    "TreasureNotFoundError",
    "WarNotFoundError",
)


class NotFoundError(BaseError):
    ...


class AllianceNotFoundError(NotFoundError):
    ...


class AttackNotFoundError(NotFoundError):
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


class ForumNotFoundError(NotFoundError):
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


class SubscriptionNotFoundError(NotFoundError):
    ...


class TargetNotFoundError(NotFoundError):
    ...


class TicketConfigNotFoundError(NotFoundError):
    ...


class TicketNotFoundError(NotFoundError):
    ...


class TreasureNotFoundError(NotFoundError):
    ...


class WarNotFoundError(NotFoundError):
    ...
