from __future__ import annotations

import datetime
from typing import TypedDict

from ...resources import Resources

__all__ = ("Bankrec",)


class Bankrec(TypedDict):
    id: int
    date: datetime.datetime
    sender_id: int
    sender_type: int
    receiver_id: int
    receiver_type: int
    banker_id: int
    note: str
    resources: Resources
    tax_id: int
