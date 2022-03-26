from __future__ import annotations

import decimal
from typing import TYPE_CHECKING

import attrs

__all__ = ("Resources",)

if TYPE_CHECKING:
    from ..types.resources import Resources as ResourcesData


@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Resources:
    money: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    coal: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    oil: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    uranium: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    iron: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    bauxite: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    lead: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    gasoline: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    munitions: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    steel: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    aluminum: decimal.Decimal = attrs.field(default=decimal.Decimal(0))
    food: decimal.Decimal = attrs.field(default=decimal.Decimal(0))

    @classmethod
    def from_dict(cls, data: ResourcesData) -> Resources:
        return cls(**data)
