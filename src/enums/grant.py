from __future__ import annotations

from enum import Enum

__all__ = ("GrantPayoff", "GrantStatus")


class GrantPayoff(Enum):
    NONE = 0
    DEPOSIT = 1
    # TAXES = 2


class GrantStatus(Enum):
    PENDING = 0
    SENT = 1
    REJECTED = 2
    CANCELLED = 3
