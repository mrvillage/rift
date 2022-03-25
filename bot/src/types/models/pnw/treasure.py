from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("Treasure",)


class Treasure(TypedDict):
    date: datetime.datetime
    data: str
