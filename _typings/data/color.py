from __future__ import annotations

from typing import List, TypedDict

__all__ = ("ColorData", "ColorDataList")


class ColorData(TypedDict):
    color: str
    bloc_name: str
    turn_bonus: int


ColorDataList = List[ColorData]
