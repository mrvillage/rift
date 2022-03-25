from __future__ import annotations

import datetime
import decimal
from typing import TypedDict

from ...resources import Resources

__all__ = ("Nation",)


class Nation(TypedDict):
    id: int
    alliance_id: int
    alliance_position: int
    name: str
    leader: str
    continent: int
    war_policy: int
    domestic_policy: int
    color: int
    num_cities: int
    score: decimal.Decimal
    flag: str
    v_mode: bool
    beige_turns: int
    espionage_available: bool
    last_active: datetime.datetime
    date: datetime.datetime
    soldiers: int
    tanks: int
    aircraft: int
    ships: int
    missiles: int
    nukes: int
    turns_since_last_city: int
    turns_since_last_project: int
    projects: int
    wars_won: int
    wars_lost: int
    tax_id: int
    alliance_seniority: int
    estimated_resources: Resources
