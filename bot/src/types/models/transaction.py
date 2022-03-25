from __future__ import annotations

import datetime
from typing import TypedDict

from ..resources import Resources

__all__ = ("Transaction",)


class Transaction(TypedDict):
    id: int
    date: datetime.datetime
    status: int
    type: int
    creator_id: int
    to_id: int
    to_type: int
    from_id: int
    from_type: int
    resources: Resources
    note: str
