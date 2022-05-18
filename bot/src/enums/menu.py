from __future__ import annotations

import enum

__all__ = (
    "MenuItemAction",
    "MenuItemStyle",
    "MenuItemType",
)


class MenuItemAction(enum.Enum):
    NONE = 0
    ADD_ROLES = 1
    REMOVE_ROLES = 2
    TOGGLE_ROLES = 3
    CREATE_TICKETS = 4
    CLOSE_TICKETS = 5
    CREATE_EMBASSIES = 6
    CLOSE_EMBASSIES = 7


class MenuItemStyle(enum.Enum):
    BLURPLE = 0
    GRAY = 1
    GREEN = 2
    RED = 3


class MenuItemType(enum.Enum):
    BUTTON = 0
    SELECT_MENU = 1
