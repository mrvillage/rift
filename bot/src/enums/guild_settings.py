from __future__ import annotations

import enum

__all__ = ("Purpose",)


class Purpose(enum.Enum):
    ALLIANCE = 0
    ALLIANCE_GOVERNMENT = 1
    ALLIANCE_MILITARY_AFFAIRS = 2
    ALLIANCE_INTERNAL_AFFAIRS = 3
    ALLIANCE_FOREIGN_AFFAIRS = 4
    ALLIANCE_ECONOMIC_AFFAIRS = 5
    BUSINESS = 6
    COMMUNITY = 7
    PERSONAL = 8
