from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

__all__ = ("Resources",)

if TYPE_CHECKING:
    import decimal

    from ..types.resources import Resources as ResourcesData


@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Resources:
    money: decimal.Decimal
    coal: decimal.Decimal
    oil: decimal.Decimal
    uranium: decimal.Decimal
    iron: decimal.Decimal
    bauxite: decimal.Decimal
    lead: decimal.Decimal
    gasoline: decimal.Decimal
    munitions: decimal.Decimal
    steel: decimal.Decimal
    aluminum: decimal.Decimal
    food: decimal.Decimal

    @classmethod
    def from_dict(cls, data: ResourcesData) -> Resources:
        return cls(**data)
