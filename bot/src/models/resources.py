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

    def to_dict(self) -> ResourcesData:
        return {
            "money": self.money,
            "coal": self.coal,
            "oil": self.oil,
            "uranium": self.uranium,
            "iron": self.iron,
            "bauxite": self.bauxite,
            "lead": self.lead,
            "gasoline": self.gasoline,
            "munitions": self.munitions,
            "steel": self.steel,
            "aluminum": self.aluminum,
            "food": self.food,
        }

    def update(self, data: Resources) -> Resources:
        self.money = data.money
        self.coal = data.coal
        self.oil = data.oil
        self.uranium = data.uranium
        self.iron = data.iron
        self.bauxite = data.bauxite
        self.lead = data.lead
        self.gasoline = data.gasoline
        self.munitions = data.munitions
        self.steel = data.steel
        self.aluminum = data.aluminum
        self.food = data.food
        return self
