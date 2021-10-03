from __future__ import annotations

from typing import List, TypedDict

__all__ = ("TreasureData", "TreasureDataList", "RawTreasureData")


class TreasureData(TypedDict):
    name: str
    color: str
    continent: str
    bonus: int
    spawndate: str
    nation: str


TreasureDataList = List[TreasureData]


class RawTreasureData(TypedDict):
    treasures: TreasureDataList
