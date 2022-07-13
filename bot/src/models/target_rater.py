from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import consts, utils

__all__ = ("TargetRater",)

if TYPE_CHECKING:
    from typing import Any, ClassVar

    from ..commands.common import CommonSlashCommand


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TargetRater:
    TABLE: ClassVar[str] = "target_raters"
    id: int
    cities: str
    infrastructure: str
    activity: str
    soldiers: str
    tanks: str
    aircraft: str
    ships: str
    missiles: str
    nukes: str
    money: str
    coal: str
    oil: str
    uranium: str
    iron: str
    bauxite: str
    lead: str
    gasoline: str
    munitions: str
    steel: str
    aluminum: str
    food: str

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
