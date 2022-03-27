from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("WarAttack",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

    from pnwkit.data import WarAttack as PnWKitWarAttack

    from ...types.models.pnw.war_attack import WarAttack as WarAttackData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class WarAttack:
    TABLE: ClassVar[str] = "war_attacks"
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

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: WarAttackData) -> WarAttack:
        ...

    def to_dict(self) -> WarAttackData:
        ...

    def update(self, data: WarAttack) -> WarAttack:
        ...

    @classmethod
    def from_data(cls, data: PnWKitWarAttack) -> WarAttack:
        if TYPE_CHECKING:
            assert isinstance(data.infradestroyed, decimal.Decimal)
            assert isinstance(data.moneystolen, decimal.Decimal)
            assert isinstance(data.city_infra_before, decimal.Decimal)
            assert isinstance(data.infra_destroyed_value, decimal.Decimal)
            assert isinstance(data.att_mun_used, decimal.Decimal)
            assert isinstance(data.def_mun_used, decimal.Decimal)
            assert isinstance(data.att_gas_used, decimal.Decimal)
            assert isinstance(data.def_gas_used, decimal.Decimal)
        return cls(
            id=int(data.id),
            date=datetime.datetime.fromisoformat(data.date),
            attacker_id=int(data.attid),
            defender_id=int(data.defid),
            type=enums.WarAttackType(data.type),
            war_id=int(data.warid),
            victor_id=int(data.victor),
            success=data.success,
            attcas1=data.attcas1,
            attcas2=data.attcas2,
            defcas1=data.defcas1,
            defcas2=data.defcas2,
            city_id=int(data.cityid),
            infrastructure_destroyed=data.infradestroyed,
            improvements_lost=data.improvementslost,
            money_stolen=data.moneystolen,
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
