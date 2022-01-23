from __future__ import annotations

from typing import Optional, TypedDict


class TreatyData(TypedDict):
    started: str
    stopped: Optional[str]
    from_: int
    to_: int
    treaty_type: str
