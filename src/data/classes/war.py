from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from ...errors import AttackNotFoundError, WarNotFoundError
from .. import query

__all__ = ("War", "Attack")

if TYPE_CHECKING:
    from typings import AttackData, WarData


class War:
    def __init__(self, data: WarData):
        self.id: int = data["id"]
        self.date: str = data["date"]
        self.reason: str = data["reason"]
        self.war_type: str = data["war_type"]
        self.active: bool = data["active"]
        self.ground_control: int = data["ground_control"]
        self.air_superiority: int = data["air_superiority"]
        self.naval_blockade: int = data["naval_blockade"]
        self.winner: int = data["winner"]
        self.turns_left: int = data["turns_left"]
        self.attacker_id: int = data["attacker_id"]
        self.attacker_alliance_id: int = data["attacker_alliance_id"]
        self.defender_id: int = data["defender_id"]
        self.defender_alliance_id: int = data["defender_alliance_id"]
        self.attacker_points: int = data["attacker_points"]
        self.defender_points: int = data["defender_points"]
        self.attacker_peace: bool = data["attacker_peace"]
        self.defender_peace: bool = data["defender_peace"]
        self.attacker_resistance: int = data["attacker_resistance"]
        self.defender_resistance: int = data["defender_resistance"]
        self.attacker_fortify: bool = data["attacker_fortify"]
        self.defender_fortify: bool = data["defender_fortify"]
        self.attacker_gas_used: float = data["attacker_gas_used"]
        self.defender_gas_used: float = data["defender_gas_used"]
        self.attacker_munitions_used: float = data["attacker_munitions_used"]
        self.defender_munitions_used: float = data["defender_munitions_used"]
        self.attacker_aluminum_used: int = data["attacker_aluminum_used"]
        self.defender_aluminum_used: int = data["defender_aluminum_used"]
        self.attacker_steel_used: int = data["attacker_steel_used"]
        self.defender_steel_used: int = data["defender_steel_used"]
        self.attacker_infra_destroyed: float = data["attacker_infra_destroyed"]
        self.defender_infra_destroyed: float = data["defender_infra_destroyed"]
        self.attacker_money_looted: float = data["attacker_money_looted"]
        self.defender_money_looted: float = data["defender_money_looted"]
        self.attacker_soldiers_killed: int = data["attacker_soldiers_killed"]
        self.defender_soldiers_killed: int = data["defender_soldiers_killed"]
        self.attacker_tanks_killed: int = data["attacker_tanks_killed"]
        self.defender_tanks_killed: int = data["defender_tanks_killed"]
        self.attacker_aircraft_killed: int = data["attacker_aircraft_killed"]
        self.defender_aircraft_killed: int = data["defender_aircraft_killed"]
        self.attacker_ships_killed: int = data["attacker_ships_killed"]
        self.defender_ships_killed: int = data["defender_ships_killed"]
        self.attacker_missiles_used: int = data["attacker_missiles_used"]
        self.defender_missiles_used: int = data["defender_missiles_used"]
        self.attacker_nukes_used: int = data["attacker_nukes_used"]
        self.defender_nukes_used: int = data["defender_nukes_used"]
        self.attacker_infra_destroyed_value: float = data[
            "attacker_infra_destroyed_value"
        ]
        self.defender_infra_destroyed_value: float = data[
            "defender_infra_destroyed_value"
        ]

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str) -> War:
        try:
            return await cls.fetch(int(argument))
        except ValueError:
            raise WarNotFoundError(argument)

    @classmethod
    async def fetch(cls, id: int, /) -> War:
        try:
            return cls(await query.query_war(id))
        except IndexError:
            raise WarNotFoundError(id)

    def _update(self, data: WarData):
        self.id: int = data["id"]
        self.date: str = data["date"]
        self.reason: str = data["reason"]
        self.war_type: str = data["war_type"]
        self.active: bool = data["active"]
        self.ground_control: int = data["ground_control"]
        self.air_superiority: int = data["air_superiority"]
        self.naval_blockade: int = data["naval_blockade"]
        self.winner: int = data["winner"]
        self.turns_left: int = data["turns_left"]
        self.attacker_id: int = data["attacker_id"]
        self.attacker_alliance_id: int = data["attacker_alliance_id"]
        self.defender_id: int = data["defender_id"]
        self.defender_alliance_id: int = data["defender_alliance_id"]
        self.attacker_points: int = data["attacker_points"]
        self.defender_points: int = data["defender_points"]
        self.attacker_peace: bool = data["attacker_peace"]
        self.defender_peace: bool = data["defender_peace"]
        self.attacker_resistance: int = data["attacker_resistance"]
        self.defender_resistance: int = data["defender_resistance"]
        self.attacker_fortify: bool = data["attacker_fortify"]
        self.defender_fortify: bool = data["defender_fortify"]
        self.attacker_gas_used: float = data["attacker_gas_used"]
        self.defender_gas_used: float = data["defender_gas_used"]
        self.attacker_munitions_used: float = data["attacker_munitions_used"]
        self.defender_munitions_used: float = data["defender_munitions_used"]
        self.attacker_aluminum_used: int = data["attacker_aluminum_used"]
        self.defender_aluminum_used: int = data["defender_aluminum_used"]
        self.attacker_steel_used: int = data["attacker_steel_used"]
        self.defender_steel_used: int = data["defender_steel_used"]
        self.attacker_infra_destroyed: float = data["attacker_infra_destroyed"]
        self.defender_infra_destroyed: float = data["defender_infra_destroyed"]
        self.attacker_money_looted: float = data["attacker_money_looted"]
        self.defender_money_looted: float = data["defender_money_looted"]
        self.attacker_soldiers_killed: int = data["attacker_soldiers_killed"]
        self.defender_soldiers_killed: int = data["defender_soldiers_killed"]
        self.attacker_tanks_killed: int = data["attacker_tanks_killed"]
        self.defender_tanks_killed: int = data["defender_tanks_killed"]
        self.attacker_aircraft_killed: int = data["attacker_aircraft_killed"]
        self.defender_aircraft_killed: int = data["defender_aircraft_killed"]
        self.attacker_ships_killed: int = data["attacker_ships_killed"]
        self.defender_ships_killed: int = data["defender_ships_killed"]
        self.attacker_missiles_used: int = data["attacker_missiles_used"]
        self.defender_missiles_used: int = data["defender_missiles_used"]
        self.attacker_nukes_used: int = data["attacker_nukes_used"]
        self.defender_nukes_used: int = data["defender_nukes_used"]
        self.attacker_infra_destroyed_value: float = data[
            "attacker_infra_destroyed_value"
        ]
        self.defender_infra_destroyed_value: float = data[
            "defender_infra_destroyed_value"
        ]


class Attack:
    def __init__(self, data: AttackData):
        self.id: int = data["id"]
        self.war_id: int = data["war_id"]
        self.date: str = data["date"]
        self.type: str = data["type"]
        self.victor: int = data["victor"]
        self.success: int = data["success"]
        self.attcas1: int = data["attcas1"]
        self.defcas1: int = data["defcas1"]
        self.attcas2: int = data["attcas2"]
        self.defcas2: int = data["defcas2"]
        self.city_id: int = data["city_id"]
        self.infra_destroyed: float = data["infra_destroyed"]
        self.improvements_lost: int = data["improvements_lost"]
        self.money_stolen: float = data["money_stolen"]
        self.loot_info: str = data["loot_info"]
        self.resistance_eliminated: int = data["resistance_eliminated"]
        self.city_infra_before: float = data["city_infra_before"]
        self.infra_destroyed_value: float = data["infra_destroyed_value"]
        self.attacker_munitions_used: float = data["attacker_munitions_used"]
        self.defender_munitions_used: float = data["defender_munitions_used"]
        self.attacker_gas_used: float = data["attacker_gas_used"]
        self.defender_gas_used: float = data["defender_gas_used"]
        self.aircraft_killed_by_tanks: int = data["aircraft_killed_by_tanks"]

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str) -> Attack:
        try:
            return await cls.fetch(int(argument))
        except ValueError:
            raise AttackNotFoundError(argument)

    @classmethod
    async def fetch(cls, id: int, /) -> Attack:
        try:
            return cls(await query.query_attack(id))
        except IndexError:
            raise AttackNotFoundError(id)

    def _update(self, data: AttackData) -> None:
        self.id: int = data["id"]
        self.war_id: int = data["war_id"]
        self.date: str = data["date"]
        self.type: str = data["type"]
        self.victor: int = data["victor"]
        self.success: int = data["success"]
        self.attcas1: int = data["attcas1"]
        self.defcas1: int = data["defcas1"]
        self.attcas2: int = data["attcas2"]
        self.defcas2: int = data["defcas2"]
        self.city_id: int = data["city_id"]
        self.infra_destroyed: float = data["infra_destroyed"]
        self.improvements_lost: int = data["improvements_lost"]
        self.money_stolen: float = data["money_stolen"]
        self.loot_info: str = data["loot_info"]
        self.resistance_eliminated: int = data["resistance_eliminated"]
        self.city_infra_before: float = data["city_infra_before"]
        self.infra_destroyed_value: float = data["infra_destroyed_value"]
        self.attacker_munitions_used: float = data["attacker_munitions_used"]
        self.defender_munitions_used: float = data["defender_munitions_used"]
        self.attacker_gas_used: float = data["attacker_gas_used"]
        self.defender_gas_used: float = data["defender_gas_used"]
        self.aircraft_killed_by_tanks: int = data["aircraft_killed_by_tanks"]
