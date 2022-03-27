from __future__ import annotations

import datetime
import decimal
from typing import TypedDict

__all__ = ("War",)


class War(TypedDict):
    id: int
    date: datetime.datetime
    reason: str
    type: int
    attacker_id: int
    attacker_alliance_id: int
    defender_id: int
    defender_alliance_id: int
    ground_control: int
    air_superiority: int
    naval_blockade: int
    winner_id: int
    turns_left: int
    attacker_action_points: int
    defender_action_points: int
    attacker_resistance: int
    defender_resistance: int
    attacker_peace: bool
    defender_peace: bool
    attacker_fortify: bool
    defender_fortify: bool
    attacker_gasoline_used: decimal.Decimal
    defender_gasoline_used: decimal.Decimal
    attacker_munitions_used: decimal.Decimal
    defender_munitions_used: decimal.Decimal
    attacker_aluminum_used: decimal.Decimal
    defender_aluminum_used: decimal.Decimal
    attacker_steel_used: decimal.Decimal
    defender_steel_used: decimal.Decimal
    attacker_infrastructure_destroyed: decimal.Decimal
    defender_infrastructure_destroyed: decimal.Decimal
    attacker_money_looted: decimal.Decimal
    defender_money_looted: decimal.Decimal
    attacker_soldiers_killed: int
    defender_soldiers_killed: int
    attacker_tanks_killed: int
    defender_tanks_killed: int
    attacker_aircraft_killed: int
    defender_aircraft_killed: int
    attacker_ships_killed: int
    defender_ships_killed: int
    attacker_missiles_used: int
    defender_missiles_used: int
    attacker_nukes_used: int
    defender_nukes_used: int
    attacker_infrastructure_destroyed_value: decimal.Decimal
    defender_infrastructure_destroyed_value: decimal.Decimal
