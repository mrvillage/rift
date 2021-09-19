from __future__ import annotations

from typing import List, TypedDict

from .alliance import AllianceData
from .city import CityData
from .color import ColorData
from .nation import NationData
from .treaty import TreatyData

__all__ = (
    "BulkAllianceListData",
    "BulkAllianceUpdateData",
    "BulkCityListData",
    "BulkCityUpdateData",
    "ColorUpdateData",
    "BulkNationListData",
    "BulkNationUpdateData",
    "BulkTreatyListData",
)

BulkAllianceListData = List[AllianceData]


class AllianceUpdateData(TypedDict):
    before: AllianceData
    after: AllianceData


BulkAllianceUpdateData = List[AllianceUpdateData]

BulkCityListData = List[CityData]


class CityUpdateData(TypedDict):
    before: CityData
    after: CityData


BulkCityUpdateData = List[CityUpdateData]

ColorUpdateData = List[ColorData]

BulkNationListData = List[NationData]


class NationUpdateData(TypedDict):
    before: NationData
    after: NationData


BulkNationUpdateData = List[NationUpdateData]

BulkTreatyListData = List[TreatyData]
