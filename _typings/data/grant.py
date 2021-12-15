from __future__ import annotations

from typing import TypedDict

__all__ = ("GrantData",)


class GrantData(TypedDict):
    id: int
    time: str
    recipient: int
    resources: str
    payoff: int
