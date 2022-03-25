from __future__ import annotations

import datetime
import decimal
from typing import TypedDict

from ...resources import Resources

__all__ = ("Alliance",)


class Alliance(TypedDict):
    id: int
    name: str
    acronym: str
    score: decimal.Decimal
    color: int
    date: datetime.datetime
    accepts_members: bool
    flag: str
    forum_link: str
    discord: str
    estimated_resources: Resources
