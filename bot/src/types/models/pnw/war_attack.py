from __future__ import annotations

import datetime
import decimal
from typing import TypedDict

__all__ = ("WarAttack",)


class WarAttack(TypedDict):
    id: int
    date: datetime.datetime
    attacker_id: int
    defender_id: int
    type: int
    war_id: int
    victor: int
    success: int
    attcas1: int
    attcas2: int
    defcas1: int
    defcas2: int
    city_id: int
    infrastructure_destroyed: decimal.Decimal
    improvements_lost: int
    money_stolen: decimal.Decimal
    loot_info: str
    resistance_eliminated: int
    city_infrastructure_before: decimal.Decimal
    infrastructure_destroyed_value: decimal.Decimal
    attacker_munitions_used: decimal.Decimal
    defender_munitions_used: decimal.Decimal
    attacker_gasoline_used: decimal.Decimal
    defender_gasoline_used: decimal.Decimal
    aircraft_killed_by_tanks: int
