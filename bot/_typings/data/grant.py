from __future__ import annotations

from typing import Optional, TypedDict

__all__ = ("GrantData",)


class GrantData(TypedDict):
    id: int
    time: str
    recipient: int
    resources: str
    alliance: int
    payoff: int
    note: Optional[str]
    deadline: Optional[str]
    paid: str
    status: int
    code: str
