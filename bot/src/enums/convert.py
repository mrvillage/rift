from __future__ import annotations

import enum

__all__ = ("ConvertType",)


class ConvertType(enum.Enum):
    # all higher types add on
    ID = 1
    STR_EQ = 2
    FUZZY = 3
