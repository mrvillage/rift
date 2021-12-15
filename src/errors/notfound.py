from .base import BaseError

__all__ = (
    "AccountNotFoundError",
    "AllianceNotFoundError",
    "AttackNotFoundError",
    "CategoryNotFoundError",
    "CityNotFoundError",
    "ColorNotFoundError",
    "DocumentNotFoundError",
    "EmbassyConfigNotFoundError",
    "EmbassyNotFoundError",
    "ForumNotFoundError",
    "GrantNotFoundError",
    "GuildNotFoundError",
    "MenuItemNotFoundError",
    "MenuNotFoundError",
    "NationNotFoundError",
    "NationOrAllianceNotFoundError",
    "RecipientNotFoundError",
    "RoleNotFoundError",
    "ServerNotFoundError",
    "SubscriptionNotFoundError",
    "TargetNotFoundError",
    "TicketConfigNotFoundError",
    "TicketNotFoundError",
    "TransactionNotFoundError",
    "TreasureNotFoundError",
    "WarNotFoundError",
)


class NotFoundError(BaseError):
    ...


class AccountNotFoundError(NotFoundError):
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


class GrantNotFoundError(NotFoundError):
    ...


class GuildNotFoundError(NotFoundError):
    ...


class MenuItemNotFoundError(NotFoundError):
    ...


class MenuNotFoundError(NotFoundError):
    ...


class NationNotFoundError(NotFoundError):
    ...


class NationOrAllianceNotFoundError(NotFoundError):
    ...


class RecipientNotFoundError(NotFoundError):
    ...


class RoleNotFoundError(NotFoundError):
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


class TransactionNotFoundError(NotFoundError):
    ...


class TreasureNotFoundError(NotFoundError):
    ...


class WarNotFoundError(NotFoundError):
    ...
