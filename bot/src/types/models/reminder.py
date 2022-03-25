from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("Reminder",)


class Reminder(TypedDict):
    id: int
    name: str
    message: str
    owner_id: int
    mention_ids: list[int]
    direct_message: bool
    date: datetime.datetime
    interval: datetime.timedelta
