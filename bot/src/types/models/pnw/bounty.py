from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("Bounty",)


class Bounty(TypedDict):
    id: int
    date: datetime.datetime
    nation_id: int
    amount: int
    type: int
