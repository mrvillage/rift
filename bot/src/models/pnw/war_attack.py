from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("WarAttack",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

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

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: WarAttackData) -> WarAttack:
        ...
