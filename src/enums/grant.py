from __future__ import annotations

from enum import Enum

__all__ = ("GrantPayoff",)

class GrantPayoff(Enum):
    NONE = 0
    TIME = 1
    DEPOSIT = 2
    # TAXES = 3
