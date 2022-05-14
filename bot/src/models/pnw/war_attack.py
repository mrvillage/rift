from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("WarAttack",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import Any, ClassVar

    from pnwkit.data import WarAttack as PnWKitWarAttack


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class WarAttack:
    TABLE: ClassVar[str] = "war_attacks"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = ("type",)
    id: int
    date: datetime.datetime
    attacker_id: int
    defender_id: int
    type: enums.WarAttackType
    war_id: int
    victor_id: int
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

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WarAttack:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: WarAttack) -> WarAttack:
        ...

    @classmethod
    def from_data(cls, data: PnWKitWarAttack) -> WarAttack:
        if TYPE_CHECKING:
            assert isinstance(data.infra_destroyed, decimal.Decimal)
            assert isinstance(data.money_stolen, decimal.Decimal)
            assert isinstance(data.city_infra_before, decimal.Decimal)
            assert isinstance(data.infra_destroyed_value, decimal.Decimal)
            assert isinstance(data.att_mun_used, decimal.Decimal)
            assert isinstance(data.def_mun_used, decimal.Decimal)
            assert isinstance(data.att_gas_used, decimal.Decimal)
            assert isinstance(data.def_gas_used, decimal.Decimal)
        return cls(
            id=data.id,
            date=data.date,
            attacker_id=data.att_id,
            defender_id=data.def_id,
            type=enums.WarAttackType(data.type),
            war_id=data.war_id,
            victor_id=data.victor,
            success=data.success,
            attcas1=data.attcas1,
            attcas2=data.attcas2,
            defcas1=data.defcas1,
            defcas2=data.defcas2,
            city_id=data.city_id,
            infrastructure_destroyed=data.infra_destroyed,
            improvements_lost=data.improvements_lost,
            money_stolen=data.money_stolen,
            loot_info=data.loot_info,
            resistance_eliminated=data.resistance_eliminated,
            city_infrastructure_before=data.city_infra_before,
            infrastructure_destroyed_value=data.infra_destroyed_value,
            attacker_munitions_used=data.att_mun_used,
            defender_munitions_used=data.def_mun_used,
            attacker_gasoline_used=data.att_gas_used,
            defender_gasoline_used=data.def_gas_used,
            aircraft_killed_by_tanks=data.aircraft_killed_by_tanks,
        )
