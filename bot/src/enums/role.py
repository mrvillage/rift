from __future__ import annotations

import enum

__all__ = ("AccessLevel",)


class AccessLevel(enum.Enum):
    GENERAL = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    LEADERSHIP = 4
