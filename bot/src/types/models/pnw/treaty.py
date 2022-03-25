from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("Treaty",)


class Treaty(TypedDict):
    id: int
    date: datetime.datetime
    type: int
    turns_left: int
    sender_id: int
    receiver_id: int
