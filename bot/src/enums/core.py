from __future__ import annotations

import enum

__all__ = ("TimestampStyle",)


class TimestampStyle(enum.Enum):
    SHORT_TIME = "t"
    LONG_TIME = "T"
    SHORT_DATE = "d"
    LONG_DATE = "D"
    SHORT_DATETIME = "f"
    LONG_DATETIME = "F"
    RELATIVE = "R"
