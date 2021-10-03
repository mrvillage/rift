from __future__ import annotations

from typing import TypedDict

__all__ = ("ResourcePriceData", "TradeOfferData", "TradePriceData")


class ResourcePriceData(TypedDict):
    resource: str
    avgprice: str
    marketindex: str
    highestbuy: TradeOfferData
    lowestbuy: TradeOfferData


class TradeOfferData(TypedDict):
    date: str
    nationid: int
    amount: int
    price: int
    totalvalue: int


class TradePriceData(TypedDict):
    credit: ResourcePriceData
    coal: ResourcePriceData
    oil: ResourcePriceData
    uranium: ResourcePriceData
    lead: ResourcePriceData
    iron: ResourcePriceData
    bauxite: ResourcePriceData
    gasoline: ResourcePriceData
    munitions: ResourcePriceData
    steel: ResourcePriceData
    aluminum: ResourcePriceData
    food: ResourcePriceData
