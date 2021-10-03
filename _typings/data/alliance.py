from __future__ import annotations

from typing import List, Optional, TypedDict

__all__ = ("AllianceData",)


class AllianceData(TypedDict):
    id: int
    found_date: str
    name: str
    acronym: str
    color: str
    rank: int
    members: int
    score: float
    officer_ids: List[int]
    heir_ids: List[int]
    leader_ids: List[int]
    avg_score: float
    flag_url: Optional[str]
    forum_url: Optional[str]
    ircchan: Optional[str]
