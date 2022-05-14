from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import cache, enums, models, utils

__all__ = ("Treasure",)

if TYPE_CHECKING:
    import datetime
    from typing import Any, ClassVar, Optional

    from pnwkit.data import Treasure as PnWKitTreasure


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Treasure:
    TABLE: ClassVar[str] = "treasures"
    PRIMARY_KEY: ClassVar[tuple[str]] = ("name",)
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = ("color", "continent")
    name: str
    color: enums.Color = attrs.field(converter=enums.Color)
    continent: enums.Continent = attrs.field(converter=enums.Continent)
    bonus: int
    spawn_date: datetime.datetime
    nation_id: int

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Treasure:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Treasure) -> Treasure:
        ...

    @classmethod
    def from_data(cls, data: PnWKitTreasure) -> Treasure:
        return cls(
            name=data.name,
            color=getattr(enums.Color, data.color.upper()),
            continent=getattr(enums.Continent, data.continent.upper()),
            bonus=data.bonus,
            spawn_date=data.spawn_date,
            nation_id=data.nation_id,
        )

    @property
    def nation(self) -> Optional[models.Nation]:
        return cache.get_nation(self.nation_id)
