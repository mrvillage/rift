from __future__ import annotations

from enum import Enum

__all__ = ("GrantPayoff",)


class GrantPayoff(Enum):
    NONE = 0
    DEPOSIT = 1
    # TAXES = 2
