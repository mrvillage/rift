from __future__ import annotations

from typing import TypedDict

__all__ = ("CityData",)


class CityData(TypedDict):
    id: int
    nation_id: int
    name: str
    capital: bool
    infrastructure: float
    max_infra: float
    land: float
