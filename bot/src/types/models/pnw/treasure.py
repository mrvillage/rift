from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("Treasure",)


class Treasure(TypedDict):
    date: datetime.datetime
    name: str
    color: int
    continent: int
    bonus: int
    spawn_date: datetime.datetime
    nation_id: int
