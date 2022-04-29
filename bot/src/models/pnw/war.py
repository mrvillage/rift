from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("War",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

    from pnwkit.data import War as PnWKitWar

    from ...types.models.pnw.war import War as WarData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class War:
    TABLE: ClassVar[str] = "wars"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = ("type",)
    id: int
    date: datetime.datetime
    reason: str
    type: enums.WarType
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

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: WarData) -> War:
        ...

    def to_dict(self) -> WarData:
        ...

    def update(self, data: War) -> War:
        ...

    @classmethod
    def from_data(cls, data: PnWKitWar) -> War:
        if TYPE_CHECKING:
            assert isinstance(data.att_gas_used, decimal.Decimal)
            assert isinstance(data.def_gas_used, decimal.Decimal)
            assert isinstance(data.att_mun_used, decimal.Decimal)
            assert isinstance(data.def_mun_used, decimal.Decimal)
            assert isinstance(data.att_alum_used, decimal.Decimal)
            assert isinstance(data.def_alum_used, decimal.Decimal)
            assert isinstance(data.att_steel_used, decimal.Decimal)
            assert isinstance(data.def_steel_used, decimal.Decimal)
            assert isinstance(data.att_infra_destroyed, decimal.Decimal)
            assert isinstance(data.def_infra_destroyed, decimal.Decimal)
            assert isinstance(data.att_money_looted, decimal.Decimal)
            assert isinstance(data.def_money_looted, decimal.Decimal)
            assert isinstance(data.att_infra_destroyed_value, decimal.Decimal)
            assert isinstance(data.def_infra_destroyed_value, decimal.Decimal)
        return cls(
            id=data.id,
            date=data.date,
            reason=data.reason,
            type=getattr(enums.WarType, data.war_type.name),
            attacker_id=data.att_id,
            attacker_alliance_id=data.att_alliance_id,
            defender_id=data.def_id,
            defender_alliance_id=data.def_alliance_id,
            ground_control=data.ground_control,
            air_superiority=data.air_superiority,
            naval_blockade=data.naval_blockade,
            winner_id=data.winner,
            turns_left=data.turns_left,
            attacker_action_points=data.att_points,
            defender_action_points=data.def_points,
            attacker_resistance=data.att_resistance,
            defender_resistance=data.def_resistance,
            attacker_peace=data.att_peace,
            defender_peace=data.def_peace,
            attacker_fortify=data.att_fortify,
            defender_fortify=data.def_fortify,
            attacker_gasoline_used=data.att_gas_used,
            defender_gasoline_used=data.def_gas_used,
            attacker_munitions_used=data.att_mun_used,
            defender_munitions_used=data.def_mun_used,
            attacker_aluminum_used=data.att_alum_used,
            defender_aluminum_used=data.def_alum_used,
            attacker_steel_used=data.att_steel_used,
            defender_steel_used=data.def_steel_used,
            attacker_infrastructure_destroyed=data.att_infra_destroyed,
            defender_infrastructure_destroyed=data.def_infra_destroyed,
            attacker_money_looted=data.att_money_looted,
            defender_money_looted=data.def_money_looted,
            attacker_soldiers_killed=data.att_soldiers_killed,
            defender_soldiers_killed=data.def_soldiers_killed,
            attacker_tanks_killed=data.att_tanks_killed,
            defender_tanks_killed=data.def_tanks_killed,
            attacker_aircraft_killed=data.att_aircraft_killed,
            defender_aircraft_killed=data.def_aircraft_killed,
            attacker_ships_killed=data.att_ships_killed,
            defender_ships_killed=data.def_ships_killed,
            attacker_missiles_used=data.att_missiles_used,
            defender_missiles_used=data.def_missiles_used,
            attacker_nukes_used=data.att_nukes_used,
            defender_nukes_used=data.def_nukes_used,
            attacker_infrastructure_destroyed_value=data.att_infra_destroyed_value,
            defender_infrastructure_destroyed_value=data.def_infra_destroyed_value,
        )
