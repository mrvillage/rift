from __future__ import annotations

from enum import Enum

__all__ = ("AccountType",)


class AccountType(Enum):
    ACCOUNT = 1
    NATION = 2
    ALLIANCE = 3
