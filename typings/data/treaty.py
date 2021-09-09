from __future__ import annotations

from typing import Optional, TypedDict


class TreatyData(TypedDict):
    started: str
    stopped: Optional[str]
    from_: int
    to: int
    treaty_type: str
