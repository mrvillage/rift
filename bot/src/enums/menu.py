from __future__ import annotations

import enum

__all__ = (
    "MenuItemAction",
    "MenuItemStyle",
    "MenuItemType",
)


class MenuItemAction(enum.Enum):
    ADD_ROLES = 0
    REMOVE_ROLES = 1
    TOGGLE_ROLES = 2
    CREATE_TICKETS = 3
    CLOSE_TICKETS = 4
    CREATE_EMBASSIES = 5
    CLOSE_EMBASSIES = 6


class MenuItemStyle(enum.Enum):
    BLURPLE = 0
    GRAY = 1
    GREEN = 2
    RED = 3


class MenuItemType(enum.Enum):
    BUTTON = 0
    SELECT_MENU = 1
