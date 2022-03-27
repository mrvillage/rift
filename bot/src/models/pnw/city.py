from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("City",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

    from pnwkit.data import City as PnWKitCity

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

    @classmethod
    def from_data(cls, data: PnWKitCity) -> City:
        if TYPE_CHECKING:
            assert isinstance(data.infrastructure, decimal.Decimal)
            assert isinstance(data.land, decimal.Decimal)
        return cls(
            id=int(data.id),
            nation_id=int(data.nation_id),
            name=data.name,
            date=datetime.datetime.fromisoformat(data.date),
            infrastructure=data.infrastructure,
            land=data.land,
            powered=data.powered,
            coal_power=data.coalpower,
            oil_power=data.oilpower,
            nuclear_power=data.nuclearpower,
            wind_power=data.windpower,
            coal_mines=data.coalmine,
            lead_mines=data.leadmine,
            bauxite_mine=data.bauxitemine,
            oil_well=data.oilwell,
            uranium_mine=data.uramine,
            iron_mines=data.ironmine,
            farms=data.farm,
            oil_refineries=data.gasrefinery,
            steel_mills=data.steelmill,
            aluminum_refineries=data.aluminumrefinery,
            munitions_factories=data.munitionsfactory,
            police_stations=data.policestation,
            hospitals=data.hospital,
            recycling_center=data.recyclingcenter,
            subways=data.subway,
            supermarkets=data.supermarket,
            banks=data.bank,
            shopping_malls=data.mall,
            stadiums=data.stadium,
            barracks=data.barracks,
            factories=data.factory,
            hangars=data.airforcebase,
            drydocks=data.drydock,
            nuke_date=datetime.datetime.fromisoformat(data.nukedate),
        )
