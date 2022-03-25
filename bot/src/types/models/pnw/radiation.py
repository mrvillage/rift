from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("Radiation",)


class Radiation(TypedDict):
    date: datetime.datetime
    data: str
