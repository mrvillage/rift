from __future__ import annotations

from typing import TypedDict

__all__ = ("TargetRater",)


class TargetRater(TypedDict):
    id: int
    cities: str
    infrastructure: str
    activity: str
    soldiers: str
    tanks: str
    aircraft: str
    ships: str
    missiles: str
    nukes: str
    money: str
    coal: str
    oil: str
    uranium: str
    iron: str
    bauxite: str
    lead: str
    gasoline: str
    munitions: str
    steel: str
    aluminum: str
    food: str
