from __future__ import annotations

import datetime
from typing import TypedDict

from ..resources import Resources

__all__ = ("Grant",)


class Grant(TypedDict):
    id: int
    date: datetime.datetime
    status: int
    recipient: int
    resources: Resources
    alliance_id: int
    note: str
    payoff_type: int
    deadline: datetime.datetime
    expiry: datetime.datetime
    paid: Resources
    payoff_code: str
    tax_bracket: int
