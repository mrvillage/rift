from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("Color",)


class Color(TypedDict):
    date: datetime.datetime
    data: str
