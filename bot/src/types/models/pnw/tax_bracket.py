from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("TaxBracket",)


class TaxBracket(TypedDict):
    id: int
    alliance_id: int
    name: str
    date: datetime.datetime
    date_modified: datetime.datetime
    last_modifier_id: int
    tax_rate: int
    resource_tax_rate: int
