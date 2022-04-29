from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("Trade",)


class Trade(TypedDict):
    id: int
    type: int
    date: datetime.datetime
    sender_id: int
    receiver_id: int
    resource: int
    amount: int
    action: int
    price: int
    accepted: bool
    date_accepted: datetime.datetime
    original_trade_id: int
