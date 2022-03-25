from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("InactiveAlert",)


class InactiveAlert(TypedDict):
    nation_id: int
    last_alert: datetime.datetime
