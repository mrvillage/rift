from __future__ import annotations

from typing import TypedDict

__all__ = ("TreasureData",)

class TreasureData(TypedDict):
    name: str
    color: str
    continent: str
    bonus: int
    spawndate: str
    nation: str
