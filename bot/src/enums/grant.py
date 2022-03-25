from __future__ import annotations

import enum

__all__ = ("GrantPayoffType", "GrantStatus")


class GrantPayoffType(enum.Enum):
    NONE = 0
    DEPOSIT = 1
    TAX = 2


class GrantStatus(enum.Enum):
    PENDING = 0
    SENT = 1
    REJECTED = 2
    CANCELLED = 3
