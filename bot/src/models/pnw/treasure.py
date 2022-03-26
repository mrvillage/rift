from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Treasure",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

    from ...types.models.pnw.treasure import Treasure as TreasureData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Treasure:
    TABLE: ClassVar[str] = "treasures"
    PRIMARY_KEY: ClassVar[str] = "name"
    name: str
    color: enums.Color = attrs.field(converter=enums.Color)
    continent: enums.Continent = attrs.field(converter=enums.Continent)
    bonus: int
    spawn_date: datetime.datetime
    nation_id: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TreasureData) -> Treasure:
        ...
