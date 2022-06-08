from __future__ import annotations

import decimal
from typing import TYPE_CHECKING

import attrs

__all__ = ("Resources",)

if TYPE_CHECKING:
    from typing import Generator

    from ..types.resources import Resources as ResourcesData


@attrs.define(weakref_slot=False, auto_attribs=True, eq=False)
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
        return data if isinstance(data, cls) else cls(**data)

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

    def __len__(self) -> int:
        return 12

    def __iter__(self) -> Generator[decimal.Decimal, None, None]:
        yield self.money
        yield self.coal
        yield self.oil
        yield self.uranium
        yield self.iron
        yield self.bauxite
        yield self.lead
        yield self.gasoline
        yield self.munitions
        yield self.steel
        yield self.aluminum
        yield self.food

    def __str__(self) -> str:
        resources = [
            i
            for i in (
                ("Money", self.money),
                ("Food", self.food),
                ("Coal", self.coal),
                ("Oil", self.oil),
                ("Uranium", self.uranium),
                ("Lead", self.lead),
                ("Iron", self.iron),
                ("Bauxite", self.bauxite),
                ("Gasoline", self.gasoline),
                ("Munitions", self.munitions),
                ("Steel", self.steel),
                ("Aluminum", self.aluminum),
            )
            if i[1] != 0
        ]
        if not resources:
            return "None"
        return ", ".join(
            f"{value:,.2f} {name}"
            if name != "Money"
            else f"${value:,.2f}"
            if value >= 0
            else f"-${-value:,.2f}"
            for name, value in resources
        )
