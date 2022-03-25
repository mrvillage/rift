from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("City",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

    from ...types.models.pnw.city import City as CityData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class City:
    TABLE: ClassVar[str] = "cities"
    id: int
    nation_id: int
    name: str
    date: datetime.datetime
    infrastructure: decimal.Decimal
    land: decimal.Decimal
    powered: bool
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
    nuke_date: datetime.datetime

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: CityData) -> City:
        ...
