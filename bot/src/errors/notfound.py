from __future__ import annotations

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
    model: str


class AccountNotFoundError(NotFoundError):
    model: str = "account"


class AllianceNotFoundError(NotFoundError):
    model: str = "alliance"


class AttackNotFoundError(NotFoundError):
    model: str = "attack"


class CategoryNotFoundError(NotFoundError):
    model: str = "category"


class CityNotFoundError(NotFoundError):
    model: str = "city"


class ColorNotFoundError(NotFoundError):
    model: str = "color"


class DocumentNotFoundError(NotFoundError):
    model: str = "document"


class EmbassyConfigNotFoundError(NotFoundError):
    model: str = "embassy config"


class EmbassyNotFoundError(NotFoundError):
    model: str = "embassy"


class ForumNotFoundError(NotFoundError):
    model: str = "forum"


class GrantNotFoundError(NotFoundError):
    model: str = "grant"


class GuildNotFoundError(NotFoundError):
    model: str = "guild"


class MenuItemNotFoundError(NotFoundError):
    model: str = "menu item"


class MenuNotFoundError(NotFoundError):
    model: str = "menu"


class NationNotFoundError(NotFoundError):
    model: str = "nation"


class NationOrAllianceNotFoundError(NotFoundError):
    model: str = "nation or alliance"


class RecipientNotFoundError(NotFoundError):
    model: str = "recipient"


class RoleNotFoundError(NotFoundError):
    model: str = "role"


class ServerNotFoundError(NotFoundError):
    model: str = "server"


class SubscriptionNotFoundError(NotFoundError):
    model: str = "subscription"


class TargetNotFoundError(NotFoundError):
    model: str = "target"


class TicketConfigNotFoundError(NotFoundError):
    model: str = "ticket config"


class TicketNotFoundError(NotFoundError):
    model: str = "ticket"


class TransactionNotFoundError(NotFoundError):
    model: str = "transaction"


class TreasureNotFoundError(NotFoundError):
    model: str = "treasure"


class WarNotFoundError(NotFoundError):
    model: str = "war"
