from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("City",)

if TYPE_CHECKING:
    import decimal
    from typing import Any, ClassVar, Optional

    from pnwkit.data import City as PnWKitCity


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class City:
    TABLE: ClassVar[str] = "cities"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    NO_UPDATE: ClassVar[tuple[str, ...]] = ("powered",)
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
    nuke_date: Optional[datetime.datetime]

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> City:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: City) -> City:
        ...

    @classmethod
    def from_data(cls, data: PnWKitCity) -> City:
        if TYPE_CHECKING:
            assert isinstance(data.infrastructure, decimal.Decimal)
            assert isinstance(data.land, decimal.Decimal)
        return cls(
            id=data.id,
            nation_id=data.nation_id,
            name=data.name,
            date=data.date,
            infrastructure=data.infrastructure,
            land=data.land,
            powered=getattr(data, "powered", False),
            coal_power=data.coal_power,
            oil_power=data.oil_power,
            nuclear_power=data.nuclear_power,
            wind_power=data.wind_power,
            coal_mines=data.coal_mine,
            lead_mines=data.lead_mine,
            bauxite_mine=data.bauxite_mine,
            oil_well=data.oil_well,
            uranium_mine=data.uranium_mine,
            iron_mines=data.iron_mine,
            farms=data.farm,
            oil_refineries=data.oil_refinery,
            steel_mills=data.steel_mill,
            aluminum_refineries=data.aluminum_refinery,
            munitions_factories=data.munitions_factory,
            police_stations=data.police_station,
            hospitals=data.hospital,
            recycling_center=data.recycling_center,
            subways=data.subway,
            supermarkets=data.supermarket,
            banks=data.bank,
            shopping_malls=data.shopping_mall,
            stadiums=data.stadium,
            barracks=data.barracks,
            factories=data.factory,
            hangars=data.hangar,
            drydocks=data.drydock,
            nuke_date=data.nuke_date,
        )
