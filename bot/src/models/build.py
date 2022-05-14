from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Build",)

if TYPE_CHECKING:
    import decimal
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Build:
    TABLE: ClassVar[str] = "builds"
    id: int
    name: str
    owner_id: int
    use_condition: str
    infrastructure: decimal.Decimal
    land: decimal.Decimal
    coal_power: int
    oil_power: int
    nuclear_power: int
    wind_power: int
    coal_mines: int
    lead_mines: int
    bauxite_mine: int
    oil_well: int
    uranium_mine: int
    iron_mines: int
    farms: int
    oil_refineries: int
    steel_mills: int
    aluminum_refineries: int
    munitions_factories: int
    police_stations: int
    hospitals: int
    recycling_center: int
    subways: int
    supermarkets: int
    banks: int
    shopping_malls: int
    stadiums: int
    barracks: int
    factories: int
    hangars: int
    drydocks: int

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Build:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Build) -> Build:
        ...
