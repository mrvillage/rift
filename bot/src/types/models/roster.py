from __future__ import annotations

import datetime
import decimal
from typing import TypedDict

__all__ = ("Roster",)


class Roster(TypedDict):
    nation_id: int
    alliance_id: int
    join_date: datetime.datetime
    time_zone: decimal.Decimal
