from __future__ import annotations

from typing import TypedDict

__all__ = ("NationData",)


class NationData(TypedDict):
    id: int
    name: str
    leader: str
    continent: int
    war_policy: int
    domestic_policy: int
    color: int
    alliance_id: int
    alliance: str
    alliance_position: int
    cities: int
    offensive_wars: int
    defensive_wars: int
    score: float
    v_mode: bool
    v_mode_turns: int
    beige_turns: int
    last_active: str
    founded: str
    soldiers: int
    tanks: int
    aircraft: int
    ships: int
    missiles: int
    nukes: int
