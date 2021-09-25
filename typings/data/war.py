from __future__ import annotations

from typing import TypedDict

__all__ = ("AttackData", "WarData")


class AttackData(TypedDict):
    id: int
    war_id: int
    date: str
    type: str
    victor: int
    success: int
    attcas1: int
    defcas1: int
    attcas2: int
    defcas2: int
    city_id: int
    infra_destroyed: float
    improvements_lost: int
    money_stolen: float
    loot_info: str
    resistance_eliminated: int
    city_infra_before: float
    infra_destroyed_value: float
    attacker_munitions_used: float
    defender_munitions_used: float
    attacker_gas_used: float
    defender_gas_used: float
    aircraft_killed_by_tanks: int


class WarData(TypedDict):
    id: int
    date: str
    reason: str
    war_type: str
    active: bool
    ground_control: int
    air_superiority: int
    naval_blockade: int
    winner: int
    turns_left: int
    attacker_id: int
    attacker_alliance_id: int
    defender_id: int
    defender_alliance_id: int
    attacker_points: int
    defender_points: int
    attacker_peace: bool
    defender_peace: bool
    attacker_resistance: int
    defender_resistance: int
    attacker_fortify: bool
    defender_fortify: bool
    attacker_gas_used: float
    defender_gas_used: float
    attacker_munitions_used: float
    defender_munitions_used: float
    attacker_aluminum_used: int
    defender_aluminum_used: int
    attacker_steel_used: int
    defender_steel_used: int
    attacker_infra_destroyed: float
    defender_infra_destroyed: float
    attacker_money_looted: float
    defender_money_looted: float
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
    attacker_infra_destroyed_value: float
    defender_infra_destroyed_value: float
