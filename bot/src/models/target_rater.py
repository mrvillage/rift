from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
import lang

from .. import consts, utils

__all__ = ("TargetRater",)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

    from ..commands.common import CommonSlashCommand


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TargetRater:
    TABLE: ClassVar[str] = "target_raters"
    id: int
    cities: str
    cities_expression: Optional[lang.Expression] = attrs.field(default=None)
    cities_expression_value: str = attrs.field(default="")
    infrastructure: str
    infrastructure_expression: Optional[lang.Expression] = attrs.field(default=None)
    infrastructure_expression_value: str = attrs.field(default="")
    activity: str
    activity_expression: Optional[lang.Expression] = attrs.field(default=None)
    activity_expression_value: str = attrs.field(default="")
    soldiers: str
    soldiers_expression: Optional[lang.Expression] = attrs.field(default=None)
    soldiers_expression_value: str = attrs.field(default="")
    tanks: str
    tanks_expression: Optional[lang.Expression] = attrs.field(default=None)
    tanks_expression_value: str = attrs.field(default="")
    aircraft: str
    aircraft_expression: Optional[lang.Expression] = attrs.field(default=None)
    aircraft_expression_value: str = attrs.field(default="")
    ships: str
    ships_expression: Optional[lang.Expression] = attrs.field(default=None)
    ships_expression_value: str = attrs.field(default="")
    missiles: str
    missiles_expression: Optional[lang.Expression] = attrs.field(default=None)
    missiles_expression_value: str = attrs.field(default="")
    nukes: str
    nukes_expression: Optional[lang.Expression] = attrs.field(default=None)
    nukes_expression_value: str = attrs.field(default="")
    money: str
    money_expression: Optional[lang.Expression] = attrs.field(default=None)
    money_expression_value: str = attrs.field(default="")
    coal: str
    coal_expression: Optional[lang.Expression] = attrs.field(default=None)
    coal_expression_value: str = attrs.field(default="")
    oil: str
    oil_expression: Optional[lang.Expression] = attrs.field(default=None)
    oil_expression_value: str = attrs.field(default="")
    uranium: str
    uranium_expression: Optional[lang.Expression] = attrs.field(default=None)
    uranium_expression_value: str = attrs.field(default="")
    iron: str
    iron_expression: Optional[lang.Expression] = attrs.field(default=None)
    iron_expression_value: str = attrs.field(default="")
    bauxite: str
    bauxite_expression: Optional[lang.Expression] = attrs.field(default=None)
    bauxite_expression_value: str = attrs.field(default="")
    lead: str
    lead_expression: Optional[lang.Expression] = attrs.field(default=None)
    lead_expression_value: str = attrs.field(default="")
    gasoline: str
    gasoline_expression: Optional[lang.Expression] = attrs.field(default=None)
    gasoline_expression_value: str = attrs.field(default="")
    munitions: str
    munitions_expression: Optional[lang.Expression] = attrs.field(default=None)
    munitions_expression_value: str = attrs.field(default="")
    steel: str
    steel_expression: Optional[lang.Expression] = attrs.field(default=None)
    steel_expression_value: str = attrs.field(default="")
    aluminum: str
    aluminum_expression: Optional[lang.Expression] = attrs.field(default=None)
    aluminum_expression_value: str = attrs.field(default="")
    food: str
    food_expression: Optional[lang.Expression] = attrs.field(default=None)
    food_expression_value: str = attrs.field(default="")

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TargetRater:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: TargetRater) -> TargetRater:
        ...

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> TargetRater:
        ...

    @classmethod
    def default_rater(cls) -> TargetRater:
        return cls(
            id=0,
            cities="(nation.num_cities / target.num_cities) * 10",
            infrastructure="(target.average_infrastructure / 500) * 5",
            activity="min((now() - target.last_active).days, 10)",
            soldiers=f"(nation.soldiers - target.soldiers) / {consts.MAX_SOLDIERS_PER_CITY} / max(nation.num_cities - target.num_cities, 1)",
            tanks=f"(nation.tanks - target.tanks) / {consts.MAX_TANKS_PER_CITY} / max(nation.num_cities - target.num_cities, 1)",
            aircraft=f"(nation.aircraft - target.aircraft) / {consts.MAX_AIRCRAFT_PER_CITY} / max(nation.num_cities - target.num_cities, 1)",
            ships=f"(nation.ships - target.ships) / {consts.MAX_SHIPS_PER_CITY} / max(nation.num_cities - target.num_cities, 1)",
            missiles="target.missiles * -2",
            nukes="target.nukes * -4",
            money="target.estimated_resources.money / 1000000",
            coal="target.estimated_resources.coal / 500",
            oil="target.estimated_resources.oil / 500",
            uranium="target.estimated_resources.uranium / 500",
            iron="target.estimated_resources.iron / 500",
            bauxite="target.estimated_resources.bauxite / 500",
            lead="target.estimated_resources.lead / 500",
            gasoline="target.estimated_resources.gasoline / 500",
            munitions="target.estimated_resources.munitions / 500",
            steel="target.estimated_resources.steel / 500",
            aluminum="target.estimated_resources.aluminum / 500",
            food="target.estimated_resources.food / 10000",
        )

    def get_rater(self, attr: str) -> lang.Expression:
        value = getattr(self, attr)
        expression: lang.Expression = getattr(self, f"{attr}_expression")
        if expression is None or value != getattr(self, f"{attr}_expression_value"):
            expression = lang.parse_expression(value)
            setattr(self, f"{attr}_expression", expression)
            setattr(self, f"{attr}_expression_value", value)
        return expression
