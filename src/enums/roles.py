from __future__ import annotations

from enum import Enum

__all__ = ("Privacy",)


class Privacy(Enum):
    PUBLIC = 0
    PRIVATE = 1
    PROTECTED = 2
