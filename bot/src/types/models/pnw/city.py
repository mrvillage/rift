from __future__ import annotations

import datetime
import decimal
from typing import TypedDict

__all__ = ("City",)


class City(TypedDict):
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
